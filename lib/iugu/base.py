# coding: utf-8
__author__ = 'horacioibrahim'

from httplib import HTTPSConnection
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


class IuguRequests(IuguApi):

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn = HTTPSConnection(config.API_HOSTNAME) # not put in instance

    def __init__(self, **options):
        super(IuguRequests, self).__init__(**options)

    # TODO: change __validation by descriptors in response
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

    # TODO: try/except HTTPConnection.request (self.conn.request)
    def get(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        self.conn.request("GET", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def post(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        self.conn.request("POST", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def put(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        self.conn.request("PUT", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def delete(self, urn, fields):
        fields.append(("api_token", self.API_TOKEN))
        params = urlencode(fields, True)
        self.conn.request("DELETE", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)
