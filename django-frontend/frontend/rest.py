'''
Defines a class for REST API calls.
The class handles the REST calls and encapsulates exception handling.
11/28/2019  Created
'''

import json
import requests
from requests.exceptions import HTTPError

class RestCall():
    '''
    This class handles the REST calls and encapsulates exception handling.
    The class supports only non-secure HTTP call, and data in JSON format.
    Class REST methods handle exceptions and return a tuple containing the HTTP response code,
    and a dictionary converted from the JSON response.
    '''

    def __init__(self, host='localhost', port=5000, timeouts=5):
        '''Initialize with a host and port, HTTP is the only protocol supported'''
        self.host_name = host
        self.host_port = port
        self.endpoint_url = f'http://{host}:{port}'
        self.timeouts = timeouts

    def get(self, endpoint):
        '''
        Issues a GET request to the endpoint of the associated host of the RestCall object.
        '''
        try:
            get_request = requests.get(url=f'{self.endpoint_url}{endpoint}', timeout=self.timeouts)
            get_request.raise_for_status()
            get_response = get_request.json()
            http_response_code = get_request.status_code
        except HTTPError as http_err_code:
            http_response_code = http_err_code
            if http_err_code == 400:
                get_response = { 'error': 'Bad Request'}
            elif http_err_code == 404:
                get_response = { 'error': 'Not found'}
            else:
                get_response = { 'error': 'Other error'}
        except Exception as err:
            get_response = { 'error': 'Internal Server Error' }
            http_response_code = 500

        return  (http_response_code, get_response)

    def post(self, endpoint, json_dictionary):
        '''
        The method takes an endpoint and a dictionary representation of JSON data.
        Issues a POST request to the endpoint of the associated host of the RestCall object.
        '''
        try:
            post_request = requests.post(url=f'{self.endpoint_url}{endpoint}', json=json_dictionary, timeout=self.timeouts)
            post_request.raise_for_status()
            post_response = post_request.json()
            http_response_code = post_request.status_code
        except HTTPError as http_err_code:
            http_response_code = http_err_code
            if http_err_code == 400:
                post_response = { 'error': 'Bad Request'}
            elif http_err_code == 404:
                post_response = { 'error': 'Not found'}
            else:
                post_response = { 'error': 'Other error'}
        except Exception as err:
            post_response = { 'error': 'Internal Server Error' }
            http_response_code = 500

        return  (http_response_code, post_response)

    def put(self):
        pass

    def delete(self, endpoint, json_dictionary):
        '''
        The method takes an endpoint and a dictionary representation of JSON data.
        Issues a DELETE request to the endpoint of the associated host of the RestCall object.
        '''
        try:
            delete_request = requests.delete(url=f'{self.endpoint_url}{endpoint}', json=json_dictionary, timeout=self.timeouts)
            delete_request.raise_for_status()
            delete_response = delete_request.json()
            http_response_code = delete_request.status_code
        except HTTPError as http_err_code:
            http_response_code = http_err_code
            if http_err_code == 400:
                delete_response = { 'error': 'Bad Request'}
            elif http_err_code == 404:
                delete_response = { 'error': 'Not found'}
            else:
                delete_response = { 'error': 'Other error'}
        except Exception as err:
            delete_response = { 'error': 'Internal Server Error' }
            http_response_code = 500

        return  (http_response_code, delete_response)
