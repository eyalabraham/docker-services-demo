'''
Define library project frontend views
11/15/2019  Created
'''
import json
import requests
from requests.exceptions import HTTPError
import os

from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .util import PatronLogin, PatronLoginForm
from .rest import RestCall


# Gather required Environment
# TODO: collect into a class and provide as a reusable one-time check object
catalog_service = os.getenv('CATALOG_DB_SERVICE', default='localhost')
borrowing_service = os.getenv('BORROW_DB_SERVICE', default='localhost')
patron_service = os.getenv('PATRON_DB_SERVICE', default='localhost')
liblogic_service = os.getenv('BORROW_LOGIC_SERVICE', default='localhost')
print(f'[Note] catalog_service=\'{catalog_service}\', borrowing_service=\'{borrowing_service}\', patron_service=\'{patron_service}\', liblogic_service=\'{liblogic_service}\'')

patron = PatronLogin()

def catalog(request):
    '''
    Library home page, the book catalog.
    Queries the catalog and the borrowing services to determine and display book catalog,
    and book inventory availability.
    The page is also the endpoint for a boorow POST request.
    '''
    session_id = request.session.get('session_id', 'None')
    request.session['previous_page'] = 'frontend-catalog'

    # Handle a book boorow POST request
    if request.method == 'POST':
        if patron.is_loggedin(session_id):
            # Get patron ID for borrowing
            patron_lib_id = patron.get_libid(session_id)

            http_result, patron_request = RestCall(patron_service, 5003).get(f'/patdb/pnum/{patron_lib_id}')
            if http_result != 200:
                request.session['alert_text'] = f'Patron database REST service error (HTTP {http_result})'
                request.session['alert_color'] = 'red'
                return redirect('frontend-alert')

            # Post the borrowing request to the library logic service
            patron_id = patron_request['patron'][0][0]
            book_id = int(request.POST['book_id'])

            post_object = {
                'borrow': {
                    'book_id': book_id,
                    'patron_id':patron_id
                }
            }

            http_result, borrow_response = RestCall(liblogic_service, 5004).post('/borrow', post_object)
            if http_result != 200 and http_result != 201:
                request.session['alert_text'] = f'Library borrowing and checkout REST service error (HTTP {http_result})'
                request.session['alert_color'] = 'red'
                return redirect('frontend-alert')
            else:
                if borrow_response['transaction'] is False:
                    request.session['alert_text'] = 'Checkout problem: please verify your maximum borrowed book count, or that you do not already have this book checked out.'
                    request.session['alert_color'] = 'red'
                    return redirect('frontend-alert')
                else:
                    return redirect(reverse('frontend-booklist'))

        return redirect(reverse('frontend-login'))

    # If not a boorow request then show the book catalog
    http_result, response = RestCall(catalog_service, 5001).get('/catdb')
    if http_result != 200:
        request.session['alert_text'] = f'Catalog database REST service error (HTTP {http_result})'
        request.session['alert_color'] = 'red'
        return redirect('frontend-alert')

    # Scan response as a list of books
    book_list = []
    for entry in response['books']:
        # Get the number of books borrowed to calculate availability
        http_result, response = RestCall(borrowing_service, 5002).get(f'/borrowdb/count/{entry[0]}')
        if http_result == 200:
            borrowed_count = response['transactions'][0][0]
            available_books = entry[3] - borrowed_count
        else:
            available_books = 0

        book = {
            'code'  :       entry[0],
            'title' :       entry[1],
            'author':       entry[2],
            'inventory':    entry[3],
            'cover' :       entry[4],
            'availability': available_books,
        }
        book_list.append(book)

    context = {
        'books': book_list,
    }

    # Render book catalog template page
    return render(request, 'frontend/catalog.html', context)

def booklist(request):
    '''
    This view support the 'My books' link.
    It is either called directly or redirected to from the borrow() view
    '''
    # Only proceed is patron is logged in
    session_id = request.session.get('session_id', 'None')
    request.session['previous_page'] = 'frontend-booklist'

    if patron.is_loggedin(session_id):

        # Get patron ID for borrowing
        patron_lib_id = patron.get_libid(session_id)

        http_result, response = RestCall(patron_service, 5003).get(f'/patdb/pnum/{patron_lib_id}')
        if http_result != 200:
            request.session['alert_text'] = f'Patron database REST service error (HTTP {http_result})'
            request.session['alert_color'] = 'red'
            return redirect('frontend-alert')

        patron_id = response['patron'][0][0]

        # Output patron's borrowed book list
        # Get list of patron's books
        http_result, patron_book_list = RestCall(borrowing_service, 5002).get(f'/borrowdb/patron/{patron_id}')
        if http_result != 200:
            request.session['alert_text'] = f'Borrowing database REST service error (HTTP {http_result})'
            request.session['alert_color'] = 'red'
            return redirect('frontend-alert')

        # Retrieve book details from library catalog using patron's borrowed book list
        else:
            book_list = []
            try:
                for entry in patron_book_list['transactions']:
                    # Get the number of books borrowed to calculate availability
                    http_result, book_details = RestCall(catalog_service, 5001).get(f'/catdb/{entry[1]}')
                    if http_result == 200:
                        book = {
                            'title'   : book_details['book'][0][1],
                            'author'  : book_details['book'][0][2],
                            'cover'   : book_details['book'][0][4],
                            'due_date': entry[4][0:17],
                        }
                        book_list.append(book)
                    else:
                        request.session['alert_text'] = f'Catalog database REST service error (HTTP {http_result})'
                        request.session['alert_color'] = 'red'
                        return redirect('frontend-alert')
            except:
                # Pass if patron_book_list is None (empty)
                pass

            context = {
                'books': book_list,
            }
            return render(request, 'frontend/booklist.html', context)

    return redirect(reverse('frontend-login'))    

# Forms:    https://docs.djangoproject.com/en/2.2/topics/forms/
# Sessions: https://docs.djangoproject.com/en/2.2/topics/http/sessions/
def login(request):
    '''
    Patron login page handler.
    After successful login, assign the user with a UUID and add to logged in session dictionary.
    '''
    # If the user is already logged in redirect with alert and don't allow another login
    session_id = request.session.get('session_id', 'None')

    if patron.is_loggedin(session_id):
        # This could be a logout POST request
        if request.method == 'POST':
            patron.logout(session_id)
            request.session.flush()
            return redirect(reverse('frontend-login'))

        # ... or a GET of the login page when a patron is already logged in
        context = {
            'form': {
                'need_login': 'no',
                'form'      : '',
                'title'     : f'{patron.get_username(session_id)}, you are already logged in.',
                'color'     : 'black',
            },
        }
        return render(request, 'frontend/login.html', context)

    # Handle form POST
    if request.method == 'POST':
        form = PatronLoginForm(request.POST)
        if form.is_valid():
            # Validate the user through the partons' database
            form_user_first_name = form.cleaned_data['user_first_name']
            form_user_last_name = form.cleaned_data['user_last_name']
            form_user_lib_id = form.cleaned_data['user_lib_id']
            qualifier = f'{form_user_first_name}_{form_user_last_name}_{form_user_lib_id}'

            http_result, user_validation = RestCall(patron_service, 5003).get(f'/patdb/test/{qualifier}')
            if http_result != 200:
                request.session['alert_text'] = f'Patrons database REST service error (HTTP {http_result})'
                request.session['alert_color'] = 'red'
                return redirect('frontend-alert')
            else:
                # Login the patron and generate unique session ID,
                # set the session cookie value and store with user name in login_list
                if user_validation['patron']:
                    request.session['session_id'] = patron.login(form_user_first_name, form_user_lib_id)
                    request.session.set_expiry(0)
                    request.session.modified = True

                    # Redirect back to the originating page after user is logged in
                    return_page = request.session.get('previous_page', 'frontend-login')
                    return redirect(reverse(return_page))
                else:
                    context = {
                        'form': {
                            'need_login': 'yes',
                            'form'      : form,
                            'title'     : 'Patron not registered or incorrect login information, please try again:',
                            'color'     : 'red',
                        },
                    }
                    return render(request, 'frontend/login.html', context)                                       

    # Handle form GET (or any other method) we'll create a blank form
    else:
        form = PatronLoginForm()

    context = {
        'form': {
            'need_login': 'yes',
            'form'      : form,
            'title'     : 'Patron login:',
            'color'     : 'black',
        },
    }
    return render(request, 'frontend/login.html', context)

def about(request):
    '''Library about page.'''
    return render(request, 'frontend/about.html')

def alert(request):
    '''
    This page displays alerts.
    Alert text and color should be stransferred using the session object, before calling
    a redirect() to the 'frontend-aler' page name
    '''
    context = {
        'alert': {
            'text' : request.session.get('alert_text', 'Unspecified.'),
            'color': request.session.get('alert_color', 'red'),
        },
    }

    request.session['alert_text'] = 'Unspecified.'
    request.session['alert_color'] = 'black'

    return render(request, 'frontend/alert.html', context)