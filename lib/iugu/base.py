# coding: utf-8
__author__ = 'horacioibrahim'

from httplib import HTTPSConnection, CannotSendRequest, ResponseNotReady, BadStatusLine
from urllib import urlencode
from json import load as json_load

# python-iugu package modules
import errors, config

class IuguApi(object):

    API_TOKEN = config.API_TOKEN

    def __init__(self, **options):
        self.account_id = options.get('account_id')
        self.api_user = options.get('api_user')
        # self.api_hostname = "api.iugu.com"
        self.api_mode_test = options.get('api_mode_test') # useful for payment_token

    def is_debug(self):
        """ Checks if debug mode is True.
        """
        return config.DEBUG

    def is_mode_test(self):
        # This is the "test mode" in API

        if self.api_mode_test is True:
            return "true"

        if self.api_mode_test is False:
            return "false"

        return str(config.API_MODE_TEST).lower()


class IuguRequests(IuguApi):

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn = HTTPSConnection(config.API_HOSTNAME) # not put in instance
    conn.timeout = 10

    def __init__(self, **options):
        super(IuguRequests, self).__init__(**options)

        if self.is_debug():
            self.conn.set_debuglevel(2)

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
        Wrapper to keep tcp connection ESTABLISHED. Rather the connection go to
        CLOSE_WAIT and raise errors CannotSendRequest
        """
        self.conn = HTTPSConnection(config.API_HOSTNAME) # reload
        self.conn.timeout = 10

    def __conn_request(self, http_verb, urn, params):
        """
        Wrapper to request/response of httplib's context
        """
        try:
            self.conn.request(http_verb, urn, params, self.headers)
        except CannotSendRequest:
            self.__reload_conn()
            self.conn.request(http_verb, urn, params, self.headers)

        try:
            response = self.conn.getresponse()
        except (IOError, BadStatusLine):
            self.__reload_conn()
            self.conn.request(http_verb, urn, params, self.headers)
            response = self.conn.getresponse()

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
