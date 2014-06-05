# coding: utf-8
__author__ = 'horacioibrahim'

from urllib import urlencode
from httplib import HTTPSConnection
from json import load as json_load
# python-iugu package modules
import base, config

class IuguCustomer(base.IuguApi):

    def __init__(self, email, **options):
        """

        :param **options: receives dict load by json

        """
        super(IuguCustomer, self).__init__(**options)
        self.id = options.get("id")
        self.email = email
        self.default_payment_method_id = options.get("default_payment_method_id")
        self.name = options.get("name")
        self.notes = options.get("notes")
        # TODO: convert str date in date type
        self.created_at = options.get("created_at")
        # TODO: convert str date in date type
        self.updated_at = options.get("updated_at")
        self.custom_variables = options.get("custom_variables")
        self.conn = base.IuguRequests()

    def create(self, name=None, notes=None, email=None, custom_variables=[]):
        """Creates a customer

        :param custom_variables: list of tuples [("local", "cup"),]
        """
        data = []
        urn = "/v1/customers"
        # data fields of charge
        data.append(("api_token", self.api_token))

        if name:
            data.append(("name", name))

        if notes:
            data.append(("notes", notes))

        if email:
            data.append(("email", email))
        else:
            data.append(("email", self.email))

        if isinstance(custom_variables, list) and len(custom_variables) > 0:
            for custom_var in custom_variables:
                data.append(("custom_variables[][name]", custom_var))

        customer = self.conn.post(urn, data)

        instance = IuguCustomer(**customer)
        instance.api_token = self.api_token

        return instance

    def get(self, customer_id):
        data = []

        # data fields of charge
        data.append(("api_token", self.api_token))
        urn = "/v1/customers/" + str(customer_id)
        customer = self.conn.get(urn, data)

        try:
            errors = customer['errors']
        except:
            errors = None

        if errors:
            raise TypeError("Customer not found")

        return IuguCustomer(**customer)

    def set(self, customer_id, name=None, notes=None): #TODO: custom_variables=[]
        """ Updates an customer that already exists
        """
        data = []
        urn = "/v1/customers/" + str(customer_id)
        data.append(("api_token", self.api_token))

        if name:
            data.append(("name", name))

        if notes:
            data.append(("notes", notes))

        #TODO: waiting support from API developers
        #for custom_var in custom_variables:
        #    key = "custom_variables[][{name}]".format(name=custom_var[0])
        #    value = custom_var[1]
        #    data.append((key, value))

        customer = self.conn.put(urn, data)

        return IuguCustomer(**customer)

    def save(self):
        return self.set(self.id, name=self.name, notes=self.notes)

    def delete(self, customer_id=None, api_token=None):
        data = []

        if self.id:
            # instance of class (saved)
            _customer_id = self.id
        else:
            if customer_id:
                _customer_id = customer_id
            else:
                # instance of class (not saved)
                raise TypeError("It's not instance of object returned because " \
                                "not possible delete.")

        if self.api_token is None:
            if api_token:
                self.api_token = api_token
            else:
                raise TypeError("Api token is required")

        data.append(("api_token", self.api_token))
        urn = "/v1/customers/" + str(_customer_id)
        customer = self.conn.delete(urn, data)

        try:
            errors = customer['errors']
        except:
            errors = None

        if errors:
            raise TypeError("Customer not found")

        return IuguCustomer(**customer)

    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None):
        data = []
        urn = urn = "/v1/customers/"
        data.append(("api_token", self.api_token))

        # Set options
        if limit:
            data.append(("limit", limit))
        if skip:
            data.append(("start", skip))
        if created_at_from:
            data.append(("created_at_from", created_at_from))
        if created_at_to:
            data.append(("created_at_to", created_at_to))
        if updated_since:
            data.append(("updated_since", updated_since))
        if query:
            data.append(("query", query))

        # TODO: sort not work fine. Waiting support of API providers
        if sort:
            assert sort is not str, "sort must be string as -name or name"

            if sort.startswith("-"):
                sort = sort[1:]
                key = "sortBy[{field}]".format(field=sort)
                data.append((key, "desc"))
            else:
                key = "sortBy[{field}]".format(field=sort)
                data.append((key, "asc"))

        customers = self.conn.get(urn, data)
        customers_objects = []

        for customer in customers["items"]:
            obj_customer = IuguCustomer(**customer)
            obj_customer.api_token = self.api_token
            customers_objects.append(obj_customer)

        return customers_objects

    remove = delete # remove for semantic of API and delete for HTTP verbs