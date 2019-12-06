'''
Catalog database service.
11/12/19    Created
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

@app.route('/catdb', methods=['GET'])
def get_all_books():
    '''
    Return all records available in the book catalog database.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE catalogdb;')
        cursor.execute('SELECT * FROM catalog;')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'catalogdb.catalog\' SELECT failed in: get_all_books()')
        abort(500)
    else:
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    return jsonify({'books': records})

@app.route('/catdb/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    '''
    Return a specific book by its database ID from the book catalog database.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE catalogdb;')
        cursor.execute(f'SELECT * FROM catalog WHERE id = {book_id};')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'catalogdb.catalog\' SELECT failed in: get_book_by_id()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'book': records})
    else:
        abort(404)

@app.route('/catdb/author/<name>', methods=['GET'])
def search_author(name):
    '''
    Search the author name field in the database for records containing the <name> text,
    and return the matching records.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE catalogdb;')
        cursor.execute(f'SELECT * FROM catalog WHERE author LIKE \'%{name}%\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'catalogdb.catalog\' SELECT failed in: search_author()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'books': records})
    else:
        abort(404)

@app.route('/catdb/title/<text>', methods=['GET'])
def search_title(text):
    '''
    Search the book title field in the database for records containing the <text> string,
    and return the matching records.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE catalogdb;')
        cursor.execute(f'SELECT * FROM catalog WHERE title LIKE \'%{text}%\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'catalogdb.catalog\' SELECT failed in: search_title()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'books': records})
    else:
        abort(404)

#
# TODO Administrative function to modify the catalog database
#      will require a different user with appropriate GRANT privileges
#
@app.route('/catdb', methods=['POST'])
def create_catalog():
    abort(404)

@app.route('/catdb', methods=['PUT'])
def modify_catalog():
    abort(404)

@app.route('/catdb', methods=['DELETE'])
def delete_catalog():
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
        'database':     'catalogdb',
        'user':         'rest',
        'password':     'password',
        'auth_plugin':  'mysql_native_password',   
    }

    app.run(debug=True, host=default_host, port=5001)

