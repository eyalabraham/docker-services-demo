'''
Book borrowing database service.
11/13/19    Created
'''
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

from mysql.connector import connect

import argparse
import time

#
# MySQL database connector initialization
# TODO: replace the sleep with a poll of the database service
#
time.sleep(20)
print('[Note] Pausing for database initialization...')

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost')
parser.add_argument('--db', default='localhost')
args = parser.parse_args()
default_host = args.host
database_service = args.db
print(f'[Note] Using host=\'{default_host}\' mysql=\'{database_service}\'')

try:
    my_database = connect(
        host=database_service,
        database='borrowdb',
        user='rest',
        password='password',
        auth_plugin='mysql_native_password')
    cursor = my_database.cursor()
    print('[Note] successfully connected to MySQL')
except Exception as e:
    print(repr(e))  # In order to avoid unicode character output issues
    print('Database \'borrowdb\' initialization failed')
    exit(1)

#
# Flask REST handlers
#
app = Flask(__name__)

@app.route('/borrowdb', methods=['GET'])
def get_all_transactions():
    '''
    Return all book borrowing transactions from the database.
    '''
    try:
        cursor.execute('USE borrowdb;')
        cursor.execute('SELECT * FROM borrowed;')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_all_transactions()')
        abort(500)

    if cursor.rowcount > 0:
        return jsonify({'transactions': records})
    else:
        abort(404)


@app.route('/borrowdb/<int:id>', methods=['GET'])
def get_transaction_by_id(id):
    '''
    Return a specific borrowing transaction by its ID.
    '''
    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE id = \'{id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_id()')
        abort(500)

    if cursor.rowcount > 0:
        return jsonify({'transaction': records})
    else:
        abort(404)

@app.route('/borrowdb/patron/<int:patron_id>', methods=['GET'])
def get_transaction_by_patron(patron_id):
    '''
    Return all borrowing transactions of a specific patron.
    '''
    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE patronId = \'{patron_id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_patron()')
        abort(500)

    if cursor.rowcount > 0:
        return jsonify({'transactions': records})
    else:
        abort(404)

@app.route('/borrowdb/due/<date>', methods=['GET'])
def get_transaction_by_due_date(date):
    '''
    Return all borrowing transactions that are listed with due date <date>.
    TODO: convert date so <= etc. comparison can be made, to find over due books etc.
    '''
    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE dateDue = \'{date}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_due_date()')
        abort(500)

    if cursor.rowcount > 0:
        return jsonify({'transactions': records})
    else:
        abort(404)

@app.route('/borrowdb/count/<int:book_id>', methods=['GET'])
def count_books_borrowed(book_id):
    '''
    Count and return the number of books borrowed (out) for a specific book ID.
    '''
    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT COUNT(*) FROM borrowed WHERE bookId = \'{book_id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: count_books_borrowed()')
        abort(500)

    if cursor.rowcount > 0:
        return jsonify({'transactions': records})
    else:
        abort(404)

@app.route('/borrowdb', methods=['POST'])
def add_borrow():
    '''
    Validate JSON representation of borrowing action and persist to database.
    Return an HTTP 201 created status if transaction is successful.
    '''
    if (not request.json or
        not 'book_id' in request.json or
        not 'patron_id' in request.json or
        not 'date_out' in request.json or
        not 'date_due' in request.json):
        abort(400)

    sql = 'INSERT INTO borrowed (bookId, patronId, dateOut, dateDue) VALUES (%s, %s, %s, %s);'
    val = (request.json['book_id'], request.json['patron_id'], request.json['date_out'], request.json['date_due'])

    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(sql, val)
        my_database.commit()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' INSERT failed in: add_borrow()')
        abort(500)

    return jsonify({'transaction': cursor.lastrowid}), 201

@app.route('/borrowdb', methods=['DELETE'])
def delete_borrow():
    '''
    Delete a book borrowing transaction.
    '''
    if (not request.json or
        not 'book_id' in request.json or
        not 'patron_id' in request.json):
        abort(400)

    try:
        cursor.execute('USE borrowdb;')
        cursor.execute(f'DELETE FROM borrowed WHERE bookId = {request.json["book_id"]} AND patronId = {request.json["patron_id"]};')
        my_database.commit()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' DELETE failed in: delete_borrow()')
        abort(500)

    return jsonify({'transaction': cursor.rowcount}), 201


#
# TODO Administrative function to modify the borrowing database
#
@app.route('/borrowdb', methods=['PUT'])
def update_borrow():
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
    app.run(debug=True, host=default_host, port=5002)

