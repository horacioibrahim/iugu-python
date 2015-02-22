# coding: utf-8
__author__ = 'horacioibrahim'

import os
from httplib import HTTPSConnection, CannotSendRequest, BadStatusLine
from urllib import urlencode
from json import load as json_load

# python-iugu package modules
import errors, config

class IuguApi(object):

    """
    Contains basics info to requests with API

    account_id:
    api_user:
    api_mode_test:
    """
    try:
        API_TOKEN = os.environ["IUGU_API_TOKEN"] #config.API_TOKEN
    except KeyError:
        raise errors.IuguConfigException("Required environment variable " \
                        "IUGU_API_TOKEN")

    def __init__(self, **options):
        self.account_id = options.get('account_id')
        self.api_user = options.get('api_user')
        self.api_mode_test = options.get('api_mode_test') # useful for payment_token

    def is_debug(self):
        """Returns debug mode in config"""
        return config.DEBUG

    def is_mode_test(self):
        """Check if api_mode_test is True or False.
        Return string of the boolean
        """

        if self.api_mode_test is True:
            return "true"

        return "false"

    def custom_variables_list(self, custom_variables):
        """Unpacking dictionary of keywords arguments and returns a list with
        data fit for to send API"""

        custom_data = [] # used to extend custom_variables in data_set()
        if isinstance(custom_variables, dict):
            # TODO: list comprehensions
            for k, v in custom_variables.items():
                custom_data.append(("custom_variables[][name]", k.lower()))
                custom_data.append(("custom_variables[][value]", v))

        if custom_data:
            return custom_data

        return None


class IuguRequests(IuguApi):

    """
    All request to API pass by here. Use the HTTP verbs for each request. For
    each method (get, post, put and delete) is need an URN and a list of fields
    its passed as list of tuples that is encoded by urlencode (e.g:
    [("field_api", "value")]

    URN: is relative path of URL http://api.iugu.com/ARG1/ARG2 where
    URN = "/ARG1/ARG2"

    All methods appends an api_token that is encoded in url params. The
    api_token is given in config.py its useful to work in sandbox mode.

    :method get: make a GET request
    :method post: make a POST request
    :method put: make a PUT request
    :method delete: make a DELETE request
    """

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    __conn = HTTPSConnection(config.API_HOSTNAME) # not put in instance
    __conn.timeout = 10

    def __init__(self, **options):
        super(IuguRequests, self).__init__(**options)

        if self.is_debug():
            # set debuglevel to HTTPSConnection
            self.__conn.set_debuglevel(2)

    def __validation(self, response, msg=None):
        """
        Validates if data returned by API contains errors json. The API returns
        by default a json with errors as field {errors: XXX}

         => http://iugu.com/referencias/api#erros
        """
        results = json_load(response)

        try:
            err = results['errors']
        except:
            err = None

        if err:
            raise errors.IuguGeneralException(value=err)
        else:
            return results

    def __reload_conn(self):
        """
        Wrapper to keep TCP connection ESTABLISHED. Rather the connection go to
        CLOSE_WAIT and raise errors CannotSendRequest or the server reply with
        empty and it raise BadStatusLine
        """
        self.__conn = HTTPSConnection(config.API_HOSTNAME) # reload
        self.__conn.timeout = 10

    def __conn_request(self, http_verb, urn, params):
        """
        Wrapper to request/response of httplib's context, reload a
        connection if presume that error will occurs and returns the response
        """
        try:
            self.__conn.request(http_verb, urn, params, self.headers)
        except CannotSendRequest:
            self.__reload_conn()
            self.__conn.request(http_verb, urn, params, self.headers)

        try:
            response = self.__conn.getresponse()
        except (IOError, BadStatusLine):
            self.__reload_conn()
            self.__conn.request(http_verb, urn, params, self.headers)
            response = self.__conn.getresponse()

        return response

    def get(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        response = self.__conn_request("GET", urn, params)
        return self.__validation(response)

    def post(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        response = self.__conn_request("POST", urn, params)
        return self.__validation(response)

    def put(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        response = self.__conn_request("PUT", urn, params)
        return self.__validation(response)

    def delete(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        response = self.__conn_request("DELETE", urn, params)
        return self.__validation(response)
