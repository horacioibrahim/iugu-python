# -*- coding: utf-8 -*-

__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors

class IuguCustomer(base.IuguApi):

    __conn = base.IuguRequests()

    def __init__(self, **options):
        """
        This class is a CRUD for customers in API

        :param **options: receives dictionary load by JSON with fields of API

          => http://iugu.com/referencias/api#clientes
        """
        super(IuguCustomer, self).__init__(**options)
        self.id = options.get("id")
        self.email = options.get("email")
        self.default_payment_method_id = options.get("default_payment_method_id")
        self.name = options.get("name")
        self.notes = options.get("notes")
        # TODO: convert str date in date type
        # year, month, day = map(int, string_date.split('-'))
        # date_converted = Date(day, month, year)
        self.created_at = options.get("created_at")
        # TODO: convert str date in date type
        self.updated_at = options.get("updated_at")
        self.custom_variables = options.get("custom_variables")
        self.payment = IuguPaymentMethod(self)

    def create(self, name=None, notes=None, email=None, custom_variables=None):
        """Creates a customer and return an IuguCustomer's instance

        :param name: customer name
        :param notes: field to post info's of an user
        :param email: required data of an user
        :param custom_variables: a dict {'key':'value'}
        """
        data = []
        urn = "/v1/customers"

        if name:
            data.append(("name", name))

        if notes:
            data.append(("notes", notes))

        if email:
            self.email = email

        if self.email:
            data.append(("email", self.email))
        else:
            raise errors.IuguGeneralException(value="E-mail required is empty")

        if custom_variables:
            custom_data = self.custom_variables_list(custom_variables)
            data.extend(custom_data)
        customer = self.__conn.post(urn, data)
        instance = IuguCustomer(**customer)

        return instance

    def set(self, customer_id, name=None, notes=None, custom_variables=None):
        """ Updates/changes a customer that already exists

        :param custom_variables: is a dict {'key':'value'}
        HINT: Use method save() at handling an instance
        """
        data = []
        urn = "/v1/customers/{customer_id}".format(customer_id=str(customer_id))

        if name:
            data.append(("name", name))

        if notes:
            data.append(("notes", notes))

        if custom_variables:
            custom_data = self.custom_variables_list(custom_variables)
            data.extend(custom_data)

        customer = self.__conn.put(urn, data)

        return IuguCustomer(**customer)

    def save(self):
        """Save updating a customer's instance"""
        return self.set(self.id, name=self.name, notes=self.notes)

    @classmethod
    def get(self, customer_id):
        """Gets one customer based in iD and returns an instance"""
        data = []
        urn = "/v1/customers/{customer_id}".format(customer_id=str(customer_id))
        customer = self.__conn.get(urn, data)
        instance = IuguCustomer(**customer)

        return instance

    @classmethod
    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None):
        """
        Get a list of customers and return a list of IuguCustomer's instances.

        :param limit: limits the number of customers returned by API (default
        and immutable of API is 100)
        :param skip: skips a numbers of customers where more recent insert
        ordering. Useful to pagination
        :param query: filters based in value (case insensitive)
        :param sort: sorts based in field. Use minus signal to determine the
        direction DESC or ASC (e.g sort="-email"). IMPORTANT: not work by API
        :return: list of IuguCustomer instances
        """
        data = []
        urn = "/v1/customers/"

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

        customers = self.__conn.get(urn, data)

        #TODO: list comprehensions
        customers_objects = []
        for customer in customers["items"]:
            obj_customer = IuguCustomer(**customer)
            customers_objects.append(obj_customer)

        return customers_objects

    def delete(self, customer_id=None):
        """Deletes a customer of instance or by id.
        And return the removed object"""
        data = []

        if self.id:
            # instance of class (customer already exist)
            _customer_id = self.id
        else:
            if customer_id:
                _customer_id = customer_id
            else:
                # instance of class (not saved)
                raise TypeError("It's not instance of object returned or " \
                                "customer_id is empty.")

        urn = "/v1/customers/" + str(_customer_id)
        customer = self.__conn.delete(urn, data)

        return IuguCustomer(**customer)

    remove = delete # remove for keep the semantic of API


class IuguPaymentMethod(object):

    """
    A customer have multiple payments methods with only one default. This class
    allows handling Payment Methods.

      => http://iugu.com/referencias/api#formas-de-pagamento-de-cliente
    """

    def __init__(self, customer, item_type="credit_card", **kwargs):
        assert isinstance(customer, IuguCustomer), "Customer invalid."
        _data = kwargs.get('data')
        self.customer_id = kwargs.get('customer_id') # useful create Payment by customer ID
        self.customer = customer
        self.description = kwargs.get('description')
        self.item_type = item_type # support only credit_card
        if _data:
            self.token = _data.get('token') # data credit card token
            self.display_number = _data.get('display_number')
            self.brand = _data.get('brand')
            self.holder_name = _data.get('holder_name')
        # self.set_as_default = kwargs.get('set_as_default')
        self.id = kwargs.get('id')

        # constructor payment
        data = kwargs.get('data')
        if data and isinstance(data, dict):
            self.payment_data = PaymentTypeCreditCard(**data)
        else:
            self.payment_data = PaymentTypeCreditCard()

        self.__conn = base.IuguRequests()

    def create(self, customer_id=None, description=None, number=None,
               verification_value=None, first_name=None, last_name=None,
               month=None, year=None, token=None, set_as_default=False):
        """ Creates a payment method for a customer and returns the own class

        :param customer_id: id of customer. You can pass in init or here
        :param description: required to create method. You can pass in init
        or here

        IMPORTANT: The API assert that data is optional, but is not real
        behavior. The values as number, verification_value, first_name, last_name,
        month and year are required args.
        """
        data = []

        # check if customer_id
        if customer_id:
            self.customer_id = customer_id
        else:
            self.customer_id = self.customer.id

        if description:
            self.description = description

        # we can create description when to instance or here (in create)
        assert self.description is not None, "description is required"

        if self.customer_id:
            urn = "/v1/customers/{customer_id}/payment_methods" \
                            .format(customer_id=str(self.customer.id))
        else:
            raise errors.IuguPaymentMethodException

        # mounting data...
        data.append(("description", self.description))
        data.append(("set_as_default", set_as_default))

        if token:
            # if has token, card data it isn't need.
            self.token = token
            data.append(("token", self.token ))
        else:
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

        response = self.__conn.post(urn, data)

        return IuguPaymentMethod(self.customer, **response)

    def get(self, payment_id, customer_id=None):
        """ Returns a payment method of an user with base payment ID"""
        data = []
        payment_id = str(payment_id)

        if customer_id is None:
            if self.customer.id:
                customer_id = self.customer.id
            else:
                raise TypeError("Customer or customer_id is not be None")

        urn = "/v1/customers/{customer_id}/payment_methods/{payment_id}".\
                format(customer_id=customer_id, payment_id=payment_id)
        response = self.__conn.get(urn, data)

        return IuguPaymentMethod(self.customer, **response)

    def getitems(self, customer_id=None):
        """
        Gets payment methods of a customer and returns a list of payment's
        methods instances (API limit is 100)
        """
        data = []

        if customer_id is None:
            customer_id = self.customer.id

        urn = "/v1/customers/{customer_id}/payment_methods".\
                format(customer_id=customer_id)

        response = self.__conn.get(urn, data)
        payments = []

        for payment in response:
            obj_payment = IuguPaymentMethod(self.customer, **payment)
            payments.append(obj_payment)

        return payments

    def set(self, payment_id, description, customer_id=None,
            set_as_default=False):
        """Updates/changes payment method with based in payment ID and customer.
        And returns object edited.

        HINT: Use save() to modify instances
        """
        data = []
        data.append(("description", description))
        data.append(("set_as_default", set_as_default))

        if customer_id is None:
            customer_id = self.customer.id

        urn = "/v1/customers/{customer_id}/payment_methods/{payment_id}".\
                format(customer_id=customer_id, payment_id=payment_id)
        response = self.__conn.put(urn, data)

        return IuguPaymentMethod(self.customer, **response)

    def save(self):
        return self.set(self.id, self.description)


    def delete(self, payment_id, customer_id=None):
        """Deletes payment method with based in ID and customer. And
        returns object edited.

        HINT: Use remove() for to remove instances
        """
        data = []

        if customer_id is None:
            customer_id = self.customer.id

        urn = "/v1/customers/{customer_id}/payment_methods/{payment_id}".\
                format(customer_id=customer_id, payment_id=payment_id)

        response = self.__conn.delete(urn, data)

        return IuguPaymentMethod(self.customer, **response)

    def remove(self):
        assert self.id is not None, "Invalid: IuguPaymentMethod not have ID."
        return self.delete(self.id)


class PaymentTypeCreditCard(object):

    """

    This class abstract the data parameter of payment method context

    :method is_valid: check if required fields is correct
    :method to_data: returns the data in format to be encoded by urllib as a
    list of tuples

    """

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
        """Required to send to API"""
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
        if not self.is_valid():
            blanks = [ k for k, v in self.__dict__.items() if v is None]
            raise TypeError("All fields required to %s. Blank fields given %s" %
                            (self.__class__, blanks))

        data = []
        for k, v in self.__dict__.items():
            key = "data[{key_name}]".format(key_name=k)
            data.append((key, v))

        return data
