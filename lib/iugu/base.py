# coding: utf-8
__author__ = 'horacioibrahim'

from httplib import HTTPSConnection
from urllib import urlencode
from json import load as json_load

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

    def get(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("GET", urn, params, self.headers)
        response = self.conn.getresponse()
        return json_load(response)

    def post(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("POST", urn, params, self.headers)
        response = self.conn.getresponse()
        return json_load(response)

    def put(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("PUT", urn, params, self.headers)
        response = self.conn.getresponse()
        return json_load(response)

    def delete(self, urn, fields):
        params = urlencode(fields, True)
        self.conn.request("DELETE", urn, params, self.headers)
        response = self.conn.getresponse()
        return json_load(response)
