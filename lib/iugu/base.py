# coding: utf-8
__author__ = 'horacioibrahim'

from httplib import HTTPSConnection
from urllib import urlencode
from json import load as json_load

# python-iugu package modules
import errors

class IuguApi(object):

    def __init__(self, **options):
        self.account_id = options.get('account_id')
        self.api_token = options.get('api_token')
        self.api_user = options.get('api_user')
        self.api_hostname = "api.iugu.com"
        self.api_mode_test = options.get('api_mode_test')


class IuguRequests(IuguApi):

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, **options):
        super(IuguRequests, self).__init__(**options)
        self.conn = HTTPSConnection(self.api_hostname)


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

    def get(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("GET", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def post(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("POST", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def put(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("PUT", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)

    def delete(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("DELETE", urn, params, self.headers)
        response = self.conn.getresponse()
        return self.__validation(response)
