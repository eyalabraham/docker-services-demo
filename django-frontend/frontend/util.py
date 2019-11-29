'''
Library project utility classes module for views.
Defines: patron login form class, patron login sessions' class.
11/23/2019  Created
'''
import uuid

from django import forms

class PatronLoginForm(forms.Form):
    '''Patron login form class associated with patron login view.'''
    user_first_name = forms.CharField(label='First name:', max_length=30)
    user_last_name = forms.CharField(label='Last name:', max_length=30)
    user_lib_id = forms.CharField(label='Library ID:', max_length=30)

class PatronLogin():
    '''
    Patron login session management class.
    Tha class tracks logins by session IDs and not by user name.
    '''

    def __init__(self):
        self.login_list = {}

    def login(self, user_name, user_id):
        '''Login a user by registering their name and returning their assigned UUID.'''
        session_id = uuid.uuid1().hex

        # Remove onld login sessions for the same user.
        # This is safe becsaue the front end will not allow two logins,
        # so anything left in this list has expired/logged-out due to browser close.
        for session in self.login_list:
            if (self.login_list[session]['user_name'] == user_name and 
                self.login_list[session]['user_lib_id'] == user_id):
                del self.login_list[session]

        # Store the new session
        self.login_list[session_id] = {'user_name':user_name, 'user_lib_id':user_id}
        return session_id

    def logout(self, session_id):
        '''Logout a user by deleting their associated entry from the dictionary.'''
        if session_id in self.login_list:
            del self.login_list[session_id]

    def get_username(self, session_id):
        '''If session is tracked return the user name for a session ID'''
        if session_id in self.login_list:
            return self.login_list[session_id]['user_name']

    def get_libid(self, session_id):
        '''If session is tracked return the library ID for a session ID'''
        if session_id in self.login_list:
            return self.login_list[session_id]['user_lib_id']

    def is_loggedin(self, session_id):
        '''Check existence of user in the login dictionary'''
        return session_id in self.login_list