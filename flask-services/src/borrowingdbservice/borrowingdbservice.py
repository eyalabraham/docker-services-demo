'''
Book borrowing database service.
11/13/19    Created
'''
import argparse
import time

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

from mysql.connector import connect
from mysql.connector import Error

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
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute('SELECT * FROM borrowed;')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_all_transactions()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'transactions': records})
    else:
        return jsonify({'transactions': None})


@app.route('/borrowdb/<int:id>', methods=['GET'])
def get_transaction_by_id(id):
    '''
    Return a specific borrowing transaction by its ID.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE id = \'{id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_id()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'transaction': records})
    else:
        return jsonify({'transaction': None})

@app.route('/borrowdb/patron/<int:patron_id>', methods=['GET'])
def get_transaction_by_patron(patron_id):
    '''
    Return all borrowing transactions of a specific patron.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE patronId = \'{patron_id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_patron()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'transactions': records})
    else:
        return jsonify({'transactions': None})

@app.route('/borrowdb/due/<date>', methods=['GET'])
def get_transaction_by_due_date(date):
    '''
    Return all borrowing transactions that are listed with due date <date>.
    TODO: convert date so <= etc. comparison can be made, to find over due books etc.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT * FROM borrowed WHERE dateDue = \'{date}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: get_transaction_by_due_date()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'transactions': records})
    else:
        return jsonify({'transactions': None})

@app.route('/borrowdb/count/<int:book_id>', methods=['GET'])
def count_books_borrowed(book_id):
    '''
    Count and return the number of books borrowed (out) for a specific book ID.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(f'SELECT COUNT(*) FROM borrowed WHERE bookId = \'{book_id}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' SELECT failed in: count_books_borrowed()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'transactions': records})
    else:
        return jsonify({'transactions': None})

@app.route('/borrowdb', methods=['POST'])
def add_borrow():
    '''
    Validate JSON representation of borrowing action and persist to database.
    Return an HTTP 201 created status if transaction is successful.
    '''
    borrow_request = request.json['borrow']

    if (borrow_request is None or
        'book_id' not in borrow_request or
        'patron_id' not in borrow_request or
        'date_out' not in borrow_request or
        'date_due' not in borrow_request):
        abort(400)

    sql = 'INSERT INTO borrowed (bookId, patronId, dateOut, dateDue) VALUES (%s, %s, %s, %s);'
    val = (borrow_request['book_id'], borrow_request['patron_id'], borrow_request['date_out'], borrow_request['date_due'])

    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(sql, val)
        my_db.commit()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' INSERT failed in: add_borrow()')
        abort(500)
    else:
        last_row_id = cursor.lastrowid
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    return jsonify({'transaction': last_row_id}), 201

@app.route('/borrowdb', methods=['DELETE'])
def delete_borrow():
    '''
    Delete a book borrowing transaction.
    '''
    return_request = request.json['return']

    if (return_request is None or
        'book_id' not in return_request or
        'patron_id' not in return_request):
        abort(400)

    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE borrowdb;')
        cursor.execute(f'DELETE FROM borrowed WHERE bookId = {return_request["book_id"]} AND patronId = {return_request["patron_id"]};')
        my_db.commit()
    except Exception as e:
        print(repr(e))
        print('Database \'borrowdb.borrowed\' DELETE failed in: delete_borrow()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    return jsonify({'transaction': row_count}), 201

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
# Database connection retry function
#
def connect_retry(user, password, database,
                  back_off_count=4, host='localhost', port=3306,
                  auth_plugin='mysql_native_password'):
    '''
    Initialize a database connection with connection parameters,
    but retry connection upon failure using a backoff count and delay.
    Use connect_retry() instead of connect() with MySQL.
    '''
    if back_off_count > 4:
        back_off_count = 4

    back_off_delay = 1

    for retry_count in range(back_off_count + 1):
        try:
            db_connection = connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                auth_plugin=auth_plugin)

        except Error as err:
            print(err, end='.')
            if retry_count == back_off_count:
                print(' Giving up.')
                continue
            # Power of 2 wait time: 1, 2, 4, 8 seconds
            time.sleep(back_off_delay)
            print(f' Retrying {retry_count+1}/{back_off_count}')
            back_off_delay = back_off_delay * 2

        else:
            break
    else:
        return None

    return db_connection

#
# Startup
#
if __name__ == '__main__':
    # Initialize module from command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--db', default='localhost')
    args = parser.parse_args()
    default_host = args.host
    database_service = args.db
    print(f'[Note] Using host=\'{default_host}\' mysql=\'{database_service}\'')

    dbconfig = {
        'host':         database_service,
        'database':     'borrowdb',
        'user':         'rest',
        'password':     'password',
        'auth_plugin':  'mysql_native_password',   
    }

    app.run(debug=True, host=default_host, port=5002)

