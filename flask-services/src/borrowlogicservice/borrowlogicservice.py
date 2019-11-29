'''
Library borroeing logic service.
11/25/19    Created
'''
import json
import requests
import argparse
from datetime import date, timedelta

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

BORROWING_LIMIT = 4

# User-defined borrowing exception classes
class Error(Exception):
   '''Base class for other exceptions'''
   pass

class BookAlreadyBorrowedException(Error):
   '''Raised when the patron already had this book borrowed'''
   pass

class BorrowingOverLimitException(Error):
   '''Raised when the patron tried to borrow books over borrowing count limit'''
   pass

class HasBookOverDueException(Error):
   '''Raised when the patron has a book that is over due'''
   pass

# Gather required service addresses
# TODO: collect into a class and provide as a reusable one-time check object
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost')
parser.add_argument('--cat', default='localhost')
parser.add_argument('--borrow', default='localhost')
args = parser.parse_args()
default_host = args.host
catalog_service = args.cat
borrowing_service = args.borrow
print(f'[Note] Using host=\'{default_host}\', catalog_service=\'{catalog_service}\', borrowing_service=\'{borrowing_service}\'')

#
# Flask REST handlers
#
app = Flask(__name__)

@app.route('/borrow', methods=['POST'])
def borrow_request():
    '''
    Validates request through library borrowing logic.
    Return an HTTP 201 created status if borrowing transaction is successful.
    Borrowing logic:
    1. Patron registered (no need to check, only logged in patrons can send borrow request)
    2. Book inventory > 0 (no need to check, only positive inventory has borrow request button)
    3. Patron does not already have the requested book
    4. Patron is not over book count limit
    5. {optional} Patron does not have an overduew book
    '''
    borrow_request = request.json['borrow']

    if (borrow_request is None or
        'book_id' not in borrow_request or
        'patron_id' not in borrow_request):
        # Reject the borrowing transaction
        return jsonify({'transaction': False})

    # Get patron's book list and process according to logic in steps 3 and 4
    book_id = request.json['borrow']['book_id']
    patron_id = request.json['borrow']['patron_id']
    try:
        patron_borrow_records = requests.get(f'http://{borrowing_service}:5002/borrowdb/patron/{patron_id}')                   
        patron_borrow_records.raise_for_status()
    except Exception as err:
        print(f'[Note] GET exception borrow_request() err={err}')
        abort(500)
    
    patron_book_list = patron_borrow_records.json()['transactions']

    # Process borrowing logic
    if patron_book_list is not None:
        try:
            # Test number 3
            for borrow_record in patron_book_list:
                if book_id == borrow_record[1]:
                    raise BookAlreadyBorrowedException
            # Test number 4
            if len(patron_book_list) == BORROWING_LIMIT:
                raise BorrowingOverLimitException

        except (BookAlreadyBorrowedException, BorrowingOverLimitException):
            return jsonify({'transaction': False})

    # Ok to borrow book
    post_url = f'http://{borrowing_service}:5002/borrowdb'
    post_object = {
        "book_id"   : book_id,
        "patron_id" : patron_id,
        "date_out"  : str(date.today()),
        "date_due"  : str(date.today() + timedelta(days=14)),
    }

    try:
        borrow_response = requests.post(url=post_url, json={'borrow':post_object})
        borrow_response.raise_for_status()
    except Exception as err:
        print(f'[Note] POST exception borrow_request() err={err}')
        abort(500)

    return jsonify({'transaction': True}), 201

@app.route('/borrow', methods=['DELETE'])
def return_request():
    abort(404)

#
# Unsopported end points
#
@app.route('/borrow', methods=['GET'])
def all_get():
    abort(404)

@app.route('/borrow', methods=['PUT'])
def modify_borrow():
    abort(404)

#
# HTTP error handlers for JSON output
#
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

#
# Startup
#
if __name__ == '__main__':
    app.run(debug=True, host=default_host, port=5004)

