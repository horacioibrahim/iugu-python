# coding: utf-8
__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors

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
        self.payment = IuguPaymentMethod(self)

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

        return IuguCustomer(**customer)

    remove = delete # remove for semantic of API and delete for HTTP verbs

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


class IuguPaymentMethod(object):

    def __init__(self, customer, item_type="credit_card", **kwargs):
        # self.customer_id = kwargs.get('customer_id')
        self.customer = customer
        self.description = kwargs.get('description')
        self.item_type = item_type # TODO **load?
        self.token = kwargs.get('token') # data credit card token
        self.set_as_default = kwargs.get('set_as_default')
        self.id = kwargs.get('id')

        # constructor payment
        data = kwargs.get('data')
        if data and isinstance(data, dict):
            self.payment_data = PaymentTypeCreditCard(**data)
        else:
            self.payment_data = PaymentTypeCreditCard()

        self.conn = base.IuguRequests()

    def create(self, customer_id=None, description=None, number=None,
               verification_value=None, first_name=None, last_name=None,
               month=None, year=None):
        """ Creates a payment method for a client

        :param customer_id: id of customer. You can pass in init or here
        :param description: required to create method. You can pass in init or here

        TODO: By API data is optional, but is not real behavior. If confirmed the
        required fields as number, verification_value, first_name, last_name,
        month and year we can put as required args.
        """
        data = []

        if customer_id:
            self.customer_id = customer_id

        if description:
            self.description = description

        assert self.description is not None, "description is required"
        assert isinstance(self.customer, IuguCustomer), "Customer invalid."

        if self.customer.id:
            urn = "/v1/customers/{customer_id}/payment_methods" \
                            .format(customer_id=str(self.customer.id))
        else:
            raise errors.IuguPaymentMethodException

        # mounting data...
        data.append(("api_token", self.customer.api_token))
        data.append(("description", self.description))
        data.append(("item_type", self.item_type ))

        if number:
            self.payment_data.number = number

        if verification_value:
            self.payment_data.verification_value = verification_value

        if first_name:
            self.payment_data.first_name = first_name

        if last_name:
            self.payment_data.last_name = last_name

        if month:
            self.payment_data.month = month

        if year:
            self.payment_data.year = year

        if self.payment_data.is_valid():
            # It's possible create payment method without credit card data.
            # Therefore this check is need.
            payment = self.payment_data.to_data()
            data.extend(payment)

        response = self.conn.post(urn, data)

        return IuguPaymentMethod(self.customer, **response)

        #payment_method = self.conn.get(urn, data)

class PaymentTypeCreditCard(object):

    def __init__(self, **kwargs):
        self.number = kwargs.get('number')
        self.verification_value = kwargs.get('verification_value')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.month = kwargs.get('month')
        self.year = kwargs.get('year')
        self.display_number = kwargs.get('display_number')
        self.token = kwargs.get('token')
        self.brand = kwargs.get('brand')

    def is_valid(self):
        if self.number and self.verification_value and self.first_name and \
            self.last_name and self.month and self.year:
            return True
        else:
            return False

    def to_data(self):
        """
        Returns a list of tuples with ("data[field]", value). Use it to
        return a data that will extend the data params in request.
        """
        # control to required fields
        if self.number and self.verification_value and self.first_name and \
            self.last_name and self.month and self.year:
            pass
        else:
            blanks = [ k for k, v in self.__dict__.items() if v is None]
            raise TypeError("All fields required to %s. Blank fields given %s" %
                            (self.__class__, blanks))
        data = []
        data.append(("data[number]", self.number))
        data.append(("data[verification_value]", self.verification_value))
        data.append(("data[first_name]", self.first_name))
        data.append(("data[last_name]", self.last_name))
        data.append(("data[month]", self.month))
        data.append(("data[year]", self.year))

        return data


