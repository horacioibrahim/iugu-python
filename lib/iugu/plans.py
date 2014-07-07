__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors

class IuguPlan(object):

    """

    This class allows handling plans. Basically contains a CRUD

    :attribute data: is a descriptor and their setters carries the rules

      => http://iugu.com/referencias/api#criar-um-plano

    """

    __conn = base.IuguRequests()

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name  = kwargs.get("name")
        self.identifier = kwargs.get("identifier")
        self.interval = kwargs.get("interval")
        self.interval_type = kwargs.get("interval_type")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.currency = kwargs.get("currency") # API move it to prices scope
        self.value_cents = kwargs.get("value_cents") # API move it to prices scope
        self._data = None
        self._prices = kwargs.get("prices")
        self.prices = []
        self._features = kwargs.get("features")
        self.features = []

        if isinstance(self._prices, list):
            for price in self._prices:
                obj_price = Price(**price)
                self.prices.append(obj_price)

        if isinstance(self._features, list):
            for feature in self._features:
                obj_feature = Feature(**feature)
                self.features.append(obj_feature)

    def is_valid(self):
        """Checks required fields to send to API.

        IMPORTANT: Only to use before send request for API. The fields currency
        and value_cents will saved in prices scope. Because not to use validate
        with returned data by API.
        """

        if self.name and self.identifier and self.interval and \
            self.interval_type and self.currency and self.value_cents:
            return True
        else:
            return False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, kwargs):
        """Defines data and validates required fields to send to API.
        Returns data as list for urlencoded.
        """
        data = []

        # required fields
        self.name = kwargs.get("name")
        self.identifier = kwargs.get("identifier")
        self.interval = kwargs.get("interval")
        self.interval_type = kwargs.get("interval_type")
        self.currency = kwargs.get("currency")
        self.value_cents = kwargs.get("value_cents")
        # optional fields
        self.prices = kwargs.get("prices")
        self.features = kwargs.get("features")

        # required fields. if not passed the API return an exception
        if self.name:
            data.append(("name", self.name))

        if self.identifier:
            data.append(("identifier", self.identifier))

        if self.interval:
            data.append(("interval", self.interval))

        if self.interval_type:
            data.append(("interval_type", self.interval_type))

        if self.currency:
            if self.currency == "BRL":
                data.append(("currency", self.currency))
            else:
                raise errors.IuguPlansException(value="Only BRL supported")

        if self.value_cents:
            data.append(("value_cents", self.value_cents))

        # optional fields
        if self.prices:
            if isinstance(self.prices, list):
                # each prices items must be instance's Price class
                for price in self.prices:
                    data.extend(price.to_data())
            else:
                raise errors.IuguPlansException(value="The fields prices must "\
                 "be a list of obj Price")

        if self.features:
            if isinstance(self.features, list):
                for feature in self.features:
                    data.extend(feature.to_data())
            else:
                raise errors.IuguPlansException(value="The fields features " \
                    "must be a list of obj Feature")

        self._data = data

    @data.deleter
    def data(self):
        del self._data

    def create(self, name=None, identifier=None, interval=None,
               interval_type=None, currency=None, value_cents=None,
               features=None, prices=None):
        """
        Creates a new plans in API and returns an IuguPlan's instance. The
        fields required are name, identifier, interval, interval_type and
        values_cents.

        :param name: name of a plan
        :param identifier: unique name identifier in API plan context
        :param interval: an integer that define duration (e.g 12 to one year)
        :param interval_type: a string with "weeks" or "months"
        :param currency: only support BRL. If different raise exception
        :param value_cents: an integer with price in cents (e.g 1000 > 10.00)
        :param prices: a list of prices. The definition in API is obscure
        :param features: details with features that must be a list with
        instance of Features
        """
        urn = "/v1/plans"

        if not name:
            if self.name:
                name = self.name
            else:
                raise errors.IuguPlansException(value="Name is required")

        if not identifier:
            if self.identifier:
                identifier = self.identifier
            else:
                raise errors.IuguPlansException(value="identifier is required")

        if not interval:
            if self.interval:
                interval = self.interval
            else:
                raise errors.IuguPlansException(value="interval is required")

        if not interval_type:
            if self.interval_type:
                interval_type = self.interval_type
            else:
                raise errors.IuguPlansException(value="interval_type is required")

        if not features:
            if self.features:
                features = self.features

        if not prices:
            if self.prices:
                prices = self.prices

        if not value_cents:
            if self.value_cents:
                value_cents = self.value_cents
            else:
                raise errors.IuguPlansException(value="value_cents is required")

        if not currency:
            if self.currency:
                currency = self.currency

        kwargs_local = locals().copy()
        kwargs_local.pop('self') # prevent error of multiple value for args
        self.data = kwargs_local
        response = self.__conn.post(urn, self.data)

        return IuguPlan(**response)

    def set(self, plan_id, name=None, identifier=None, interval=None,
               interval_type=None, currency=None, value_cents=None,
               features=None, prices=None):
        """
        Edits/changes existent plan and returns IuguPlan's instance

        :param plan_id: ID number of a existent plan
        """
        urn = "/v1/plans/{plan_id}".format(plan_id=plan_id)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self.__conn.put(urn, self.data)
        return IuguPlan(**response)

    def save(self):
        """Saves an instance of IuguPlan and return own class instance
        modified"""
        urn = "/v1/plans/{plan_id}".format(plan_id=self.id)
        self.data = self.__dict__
        response = self.__conn.put(urn, self.data)
        return IuguPlan(**response)

    @classmethod
    def get(self, plan_id):
        """Gets one plan based in ID and returns an instance"""
        data = []
        urn = "/v1/plans/{plan_id}".format(plan_id=plan_id)
        response = self.__conn.get(urn, data)
        return IuguPlan(**response)

    @classmethod
    def get_by_identifier(self, identifier):
        """Gets one plan based in identifier and returns an instance

        :param identifier: it's an unique identifier plan in API
        """
        data = []
        urn = "/v1/plans/identifier/{identifier}".format(identifier=identifier)
        response = self.__conn.get(urn, data)
        return IuguPlan(**response)

    @classmethod
    def getitems(self, limit=None, skip=None, query=None, updated_since=None,
                 sort=None):
        """
        Gets plans by API default limited 100.

        :param limit: limits the number of plans returned by API (default
        and immutable of API is 100)
        :param skip: skips a numbers of plans where more recent insert
        ordering. Useful to pagination.
        :param query: filters based in value (case insensitive)
        :param sort: sorts based in field. Use minus signal to determine the
        direction DESC or ASC (e.g sort="-email"). IMPORTANT: not work by API
        :return: list of IuguPlan's instances
        """
        data = []
        urn = "/v1/plans/"

        # Set options
        if limit:
            data.append(("limit", limit))

        if skip:
            data.append(("start", skip))

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

        plans = self.__conn.get(urn, data)
        plans_objects = []
        for plan_item in plans["items"]:
            obj_plan = IuguPlan(**plan_item)
            plans_objects.append(obj_plan)

        return plans_objects

    def remove(self, plan_id=None):
        """
        Removes an instance or passing a plan_id
        """
        if plan_id:
            to_remove = plan_id
        else:
            to_remove = self.id

        if not to_remove:
            raise errors.IuguPlansException(value="Instance or plan id is required")

        urn = "/v1/plans/{plan_id}".format(plan_id=to_remove)
        response = self.__conn.delete(urn, [])
        # check if result can to generate instance of IuguPlan
        obj = IuguPlan(**response)

        if obj:
            for k, v in self.__dict__.items():
                self.__dict__[k] = None


class Price(object):

    """

    This class is useful for handling field prices of API. Prices in API is a
    field of plans context it contains list of values with some fields
    exclusively returned by API.

    :method is_valid: check if required fields are correct
    :method to_data: returns a list of tuples for urlencoded

    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.plan_id = kwargs.get("plan_id")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.value_cents = kwargs.get("value_cents")
        self.currency = kwargs.get("currency")

    def is_valid(self):
        """Required fields to send to API"""
        if self.value_cents and self.currency:
            return True
        else:
            return False

    def to_data(self):
        """
        Returns a list of tuples with ("prices[field]", value). Use it to
        return a data that will extend the data params in request.
        """
        if not self.is_valid():
            blanks = [ k for k, v in self.__dict__.items() if v is None]
            raise TypeError("All fields are required to %s. Blanks fields given %s" %
                            (self.__class__, blanks))

        data = []
        for k, v in self.__dict__.items():
            if v is not None:
                key = "prices[][{key_name}]".format(key_name=k)
                data.append((key, v))

        return data


class Feature(object):

    """

    This class abstract features of Plan context.

    :method is_valid: check if required fields are correct
    :method to_data: returns a list of tuples for urlencoded
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.identifier = kwargs.get("identifier")
        self.important = kwargs.get("important")
        self.name = kwargs.get("name")
        self.plan_id = kwargs.get("plan_id")
        self.position = kwargs.get("position")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.value = kwargs.get("value")

    def is_valid(self):
        """
        Required to send to API
        """
        if self.name and self.identifier and self.value > 0:
            return True
        else:
            return False

    def to_data(self):
        """
        Returns a list of tuples with ("features[field]", value). Use it to
        return a data that will extend the data params in request.
        """
        if not self.is_valid():
            blanks = [ k for k, v in self.__dict__.items() if v is None ]
            raise TypeError("All fields are required to class %s. Blanks fields given %s" %
                        (self.__class__, blanks))

        data = []
        for k, v in self.__dict__.items():
            if v is not None:
                key = "features[][{key_name}]".format(key_name=k)
                data.append((key, v))
        return data
