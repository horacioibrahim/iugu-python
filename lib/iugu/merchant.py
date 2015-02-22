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
        self.__conn = base.IuguRequests()

    def create_payment_token(self, card_number, first_name, last_name,
                             month, year, verification_value, method="credit_card"):
        """Sends credit_card data of a customer and returns a token
        for payment process without needing to persist personal data
        of customers.

        :param method: string 'credit_card' or options given by API.
        :param card_number: str of card number
        :param first_name: string with consumer/buyer first name
        :param last_name: consumer/buyer last name
        :param month: two digits to Month expiry date of card
        :param year: four digits to Year expiry date of card
        :param verification_value: CVV
        :returns: token_id as id, response, extra_info and method

          => http://iugu.com/referencias/api#tokens-e-cobranca-direta
        """
        urn = "/v1/payment_token"
        data = [('data[last_name]', last_name), ('data[first_name]', first_name),
                ('data[verification_value]', verification_value),
                ('data[month]', month), ('data[year]', year),
                ('data[number]', card_number)]

        data.append(("account_id", self.account_id)) # work less this
        data.append(("test", self.is_mode_test()))
        data.append(("method", method))
        token_data = self.__conn.post(urn, data)

        return Token(token_data)

    def create_charge(self, consumer_email, items, token=None, payer=None):
        """
        Creates an invoice and returns a direct charge done.

        :param token: an instance of Token. It's used to credit card payments.
        If argument token is None it's used to method=bank_slip
        """
        # TODO: payer and address support
        data = [] # data fields of charge. It'll encode
        urn = "/v1/charge"

        if isinstance(items, list):
            for item in items:
                assert type(item) is Item
                data.extend(item.to_data())
        else:
            assert type(items) is Item
            data.extend(items.to_data())

        if token and isinstance(token, Token):
            token_id = token.id
            data.append(("token", token_id))
        else:
            data.append(("method", "bank_slip"))

        data.append(("email", consumer_email))
        results = self.__conn.post(urn, data)

        return Charge(results)


class Charge(object):

    """
    This class receives response of request create_charge. Useful only to view
    status and invoice_id

    :attribute invoice_id: ID of Invoice created

    """

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

    """

    This class is representation of payment method to API.

    """
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
        if 'test' in self.token_data.keys() and self.token_data['test'] == True:
            return True
        else:
            return False

    @property
    def status(self):
        try:
            if 'errors' in self.token_data.keys():
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
        #useful for subscriptions subitems
        self.recurrent = kwargs.get("recurrent") # boolean
        self.total = kwargs.get("total")
        # command for eliminate an item
        self.destroy = None

    def __str__(self):
        return "%s" % self.description

    def to_data(self, is_subscription=False):
        """
        Returns tuples to encode with urllib.urlencode
        """
        as_tuple = []
        key = "items"

        if is_subscription is True:
            key = "subitems" # run to adapt the API subscription

        if self.id:
            as_tuple.append(("{items}[][id]".format(items=key), self.id))

        as_tuple.append(("{items}[][description]".format(items=key),
                         self.description))
        as_tuple.append(("{items}[][quantity]".format(items=key),
                         self.quantity))
        as_tuple.append(("{items}[][price_cents]".format(items=key),
                         self.price_cents))

        if self.recurrent:
            value_recurrent = str(self.recurrent)
            value_recurrent = value_recurrent.lower()
            as_tuple.append(("{items}[][recurrent]".format(items=key),
                             value_recurrent))

        if self.destroy is not None:
            value_destroy = str(self.destroy)
            value_destroy = value_destroy.lower()
            as_tuple.append(("{items}[][_destroy]".format(items=key),
                            value_destroy))

        return as_tuple

    def remove(self):
        """
        Marks the item that will removed after save an invoice
        """
        self.destroy = True


class Transfers(object):

    __conn = base.IuguRequests()
    __urn = "/v1/transfers"

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.created_at = kwargs.get("created_at")
        self.amount_cents = kwargs.get("amount_cents")
        self.amount_localized = kwargs.get("amount_localized")
        self.receiver = kwargs.get("receiver")
        self.sender = kwargs.get("sender")

    def send(self, receiver_id, amount_cents):
        """
        To send amount_cents to receiver_id
        """
        data =[]
        data.append(("receiver_id", receiver_id))
        data.append(("amount_cents", amount_cents))
        response = self.__conn.post(self.__urn, data)
        return Transfers(**response)

    @classmethod
    def getitems(self):
        """
        Gets sent and received transfers for use in API_KEY
        """
        response = self.__conn.get(self.__urn, [])
        sent = response["sent"]
        received = response["received"]
        transfers = []

        for t in sent:
            transfer_obj = Transfers(**t)
            transfers.append(transfer_obj)

        for r in received:
            transfer_obj = Transfers(**r)
            transfers.append(transfer_obj)

        return transfers
