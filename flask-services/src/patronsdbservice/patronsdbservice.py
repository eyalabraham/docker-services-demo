'''
Patrons' database service.
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
print('[Note] Pausing for database initialization...')
time.sleep(20)

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
        database='patronsdb',
        user='rest',
        password='password',
        auth_plugin='mysql_native_password')
    cursor = my_database.cursor()
    print('[Note] successfully connected to MySQL')
except Exception as e:
    print(repr(e))  # In order to avoid unicode character output issues
    print('Database \'patronsdb\' initialization failed')
    exit(1)

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
        cursor.execute('USE patronsdb;')
        cursor.execute('SELECT * FROM patrons;')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_all_patrons()')
        abort(500)

    return jsonify({'patrons': records})

@app.route('/patdb/pnum/<patron_num>', methods=['GET'])
def get_patron_by_id(patron_num):
    '''
    Return a specific patron by its library ID (12 character string) from the patrons' database.
    '''
    try:
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT id,firstName,lastName FROM patrons WHERE patronNum = \'{patron_num}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_patron_by_id()')
        abort(500)

    if cursor.rowcount > 0:
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
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT * FROM patrons WHERE firstName LIKE \'%{name}%\' OR lastName LIKE \'%{name}%\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: get_patron_by_name()')
        abort(500)

    if cursor.rowcount > 0:
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
        cursor.execute('USE patronsdb;')
        cursor.execute(f'SELECT * FROM patrons WHERE firstName = \'{qualifiers[0]}\' AND  \
                                                     lastName  = \'{qualifiers[1]}\' AND  \
                                                     BINARY patronNum = \'{qualifiers[2]}\';')
        records = cursor.fetchall()
    except Exception as e:
        print(repr(e))
        print('Database \'patronsdb.patrons\' SELECT failed in: test_patron()')
        abort(500)

    if cursor.rowcount == 1:
        return jsonify({'patron': True})
    else:
        return jsonify({'patron': False})

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
    app.run(debug=True, host=default_host, port=5003)

