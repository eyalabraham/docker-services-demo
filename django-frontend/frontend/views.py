'''
Define library project frontend views
11/15/2019  Created
'''
from django.shortcuts import render

import json
import requests
import os

def catalog(request):
    '''
    Library home page, the book catalog.
    Queries the catalog and the borrowing services to determine and display book catalog,
    and book inventory availability.
    '''
    # Gather required Environment
    # TODO: collect into a class and provide as a reusable object
    catalog_service = os.getenv('CATALOG_DB_SERVICE', default='0.0.0.0')
    borrowing_service = os.getenv('BORROW_DB_SERVICE', default='0.0.0.0')
    print(f'[Note] catalog_service=\'{catalog_service}\' borrowing_service=\'{borrowing_service}\'')

    # Request the book list from the catalog services
    try:
        catalog_request = requests.get(f'http://{catalog_service}:5001/catdb')
    except:
        context = {
            'error': {
                'text' : 'Catalog database REST service error',
                'color': 'red',
            },
        }
        return render(request, 'frontend/error.html', context)

    response = catalog_request.json()
    # Convert JSON response to a list of dictionaries
    book_list = []
    for entry in response['books']:
        # Get the number of books borrowed to calculate availability
        try:
            borrow_request = requests.get(f'http://{borrowing_service}:5002/borrowdb/count/{entry[0]}')
            if borrow_request.status_code == 200:
                borrowed_count = borrow_request.json()['transactions'][0][0]
                available_books = entry[3] - borrowed_count
            else:
                available_books = 0
        except:
            available_books = 0
        book = {
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

def about(request):
    '''Library about page.'''
    return render(request, 'frontend/about.html')

def error(request):
    '''REST service error page.'''
    return render(request, 'frontend/error.html')