'''
Patrons' database service.
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

@app.route('/patdb', methods=['GET'])
def get_all_patrons():
    '''
    Return all records of patron names from database.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE patronsdb;')
        cursor.execute('SELECT * FROM patrons;')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_all_patrons()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'patron': records})
    else:
        abort(404)

@app.route('/patdb/pnum/<patron_num>', methods=['GET'])
def get_patron_by_id(patron_num):
    '''
    Return a specific patron by its library ID (12 character string) from the patrons' database.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT id,firstName,lastName FROM patrons WHERE patronNum = \'{patron_num}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_patron_by_id()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'patron': records})
    else:
        abort(404)

@app.route('/patdb/key/<name>', methods=['GET'])
def get_patron_by_name(name):
    '''
    Search the patrons' database for patrons with a first or last name matching the <name> key,
    and return their records.
    '''
    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT * FROM patrons WHERE firstName LIKE \'%{name}%\' OR lastName LIKE \'%{name}%\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_patron_by_name()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count > 0:
        return jsonify({'patrons': records})
    else:
        abort(404)

@app.route('/patdb/test/<qualifier>', methods=['GET'])
def test_patron(qualifier):
    '''
    Search the patrons' database for a full match between the <qualifier> and
    a patron's first, last and registration ID.
    If a no matches or a single match is found return a valid JSON status response,
    if more than one match is founr signal an error.
    The <qualifier> string format is: '<patron_first_name>_<patron_last_name>_<patron_membership_num>'
    '''
    qualifiers = qualifier.split('_')
    if len(qualifiers) != 3:
        abort(400)

    try:
        my_db = connect_retry(**dbconfig)
        cursor = my_db.cursor()
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT * FROM patrons WHERE firstName = \'{qualifiers[0]}\' AND  \
                                                     lastName  = \'{qualifiers[1]}\' AND  \
                                                     BINARY patronNum = \'{qualifiers[2]}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: test_patron()')
        abort(500)
    else:
        row_count = cursor.rowcount
        if my_db.is_connected():
            cursor.close()
            my_db.close()

    if row_count == 1:
        return jsonify({'patron': True})
    else:
        return jsonify({'patron': False})

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
# TODO Administrative function to modify the patrons' database
#      will require a different user with appropriate GRANT privileges
#
@app.route('/patdb', methods=['POST'])
def create_patron():
    abort(404)

@app.route('/patdb', methods=['PUT'])
def modify_patron():
    abort(404)

@app.route('/patdb', methods=['DELETE'])
def delete_patron():
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
        'database':     'patronsdb',
        'user':         'rest',
        'password':     'password',
        'auth_plugin':  'mysql_native_password',   
    }

    app.run(debug=True, host=default_host, port=5003)

