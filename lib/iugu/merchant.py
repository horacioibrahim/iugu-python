# coding: utf-8

import httplib
import json
from urllib import urlencode
from urllib2 import urlopen, Request

# python-iugu package modules
import base, config

class IuguMerchant(base.IuguApi):

    def __init__(self, **kwargs):
        super(IuguMerchant, self).__init__(**kwargs)
        self.conn = base.IuguRequests()

    def is_debug(self):
        """ Checks if debug mode is True. This is the "test mode" in API
        """
        if self.api_mode_test:
            return str(True).lower()

        return str(config.DEBUG).lower()

    def create_payment_token(self, card_number, first_name, last_name,
                             month, year, verification_value, method="credit_card"):
        """ Returns a token for payment process

        :param method: string 'credit_card' or options given by API.
        :param card_number: str of card number
        :param first_name: string with consumer/buyer first name
        :param last_name: consumer/buyer last name
        :param month: two digits input to Month expiry date of card
        :param year: four digits input to Year expiry date of card
        :param verification_value: CVV
        :returns: token_id as id, response, extra_info and method
        """
        urn = "/v1/payment_token"
        data = [('data[last_name]', last_name), ('data[first_name]', first_name),
                ('data[verification_value]', verification_value),
                ('data[month]', month), ('data[year]', year),
                ('data[number]', card_number)]
        data.append(("account_id", self.account_id))
        data.append(("test", self.is_debug()))
        data.append(("method", method))
        token_data = self.conn.post(urn, data)

        return Token(token_data)

    def create_charge(self, consumer_email, items,
                      token=None, payer=None):
        """
        Creates an invoice

        :param token: used to credit card payments. If None it's used to
        method=bank_slip
        """
        data = [] # data fields of carge. It'll encode

        if isinstance(items, list):
            for item in items:
                assert type(item) is Item
                data.extend(item.to_data())
        else:
            assert type(items) is Item
            data.extend(items.to_data())

        urn = "/v1/charge"
        # data fields of charge
        data.append(("api_token", self.api_token))

        if token:
            data.append(("token", token))
        else:
            data.append(("method", "bank_slip"))

        data.append(("email", consumer_email))
        results = self.conn.post(urn, data)

        return Invoice(results)

class Invoice(object):

    def __init__(self, invoice):
        self.invoice = invoice

        if 'message' in invoice:
            self.message = invoice['message']

        if 'errors' in invoice:
            self.errors = invoice['errors']

        if 'success' in invoice:
            self.success = invoice['success']

        if 'invoice_id' in invoice:
            self.invoice_id = invoice['invoice_id']

    def is_success(self):
        try:
            if self.success == True:
                return True
        except:
            pass

        return False


class Token(object):

    def __init__(self, token_data):
        self.token_data = token_data

        if 'id' in token_data:
            self.id = token_data['id']
        if 'extra_info' in token_data:
            self.extra_info = token_data['extra_info']
        if 'method' in token_data:
            self.method = token_data['method']

    @property
    def is_test(self):
        if self.token_data['test'] == True:
            return True
        else:
            return False

    @property
    def status(self):
        try:
            if self.token_data['errors']:
                return self.token_data['errors']
        except:
            pass

        return 200


class Payer(object):

    def __init__(self, name, email, address=None, cpf_cnpj=None, phone_prefix=None, phone=None):
        self.cpf_cnpj = cpf_cnpj
        self.name = name
        self.email = email
        self.phone_prefix = phone_prefix
        self.phone = phone

        if isinstance(address, Address):
            self.address = address


class Address(object):

    def __init__(self, street, number, city, state, country, zip_code):
        self.street = street
        self.number = number
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code


class Item(object):

    def __init__(self, description, quantity, price_cents, **kwargs):
        self.description = description
        self.quantity = quantity
        self.price_cents = price_cents # must be integer 10.90 => 1090
        self.id = kwargs.get("id")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.price = kwargs.get("price")

    def to_data(self):
        """
        Returns tuples to encode with urllib.urlencode
        """
        as_tuple = []
        as_tuple.append(("items[][description]", self.description))
        as_tuple.append(("items[][quantity]", self.quantity))
        as_tuple.append(("items[][price_cents]", self.price_cents))
        return as_tuple

