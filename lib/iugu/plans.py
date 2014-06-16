__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors

class IuguPlan(object):

    API_TOKEN = config.API_TOKEN
    conn = base.IuguRequests()

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
        """ Required fields to send to API. Remember that currency and
        value_cents will saved in prices scope. Because not to use validate
        with returned data of API.
        IMPORTANT: This is useful before send for API.
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
        """ Prepares and validates required fields to send to API as urlencoded
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
        if self.is_valid():
            data.append(("name", self.name))
            data.append(("identifier", self.identifier))
            data.append(("interval", self.interval))
            data.append(("interval_type", self.interval_type))
            data.append(("currency", self.currency))
            data.append(("value_cents", self.value_cents))
        else:
            # for prevent request in API with incomplete data
            raise errors.IuguPlansException

        # optional fields
        if self.prices:
            if isinstance(self.prices, list):
                # each prices items must be instance's Price class
                for price in self.prices:
                    data.extend(price.to_data())
            else:
                raise TypeError("The fields prices must be a list of obj Price")

        if self.features:
            if isinstance(self.features, list):
                for feature in self.features:
                    data.extend(feature.to_data())
            else:
                raise TypeError("The fields features must be a list of obj Feature")

        self._data = data

    @data.deleter
    def data(self):
        del self._data

    def create(self, name=None, identifier=None, interval=None,
               interval_type=None, currency=None, value_cents=None,
               features=None, prices=None):
        """
        Creates a new plans
        """
        urn = "/v1/plans"
        kwargs_local = locals().copy()
        kwargs_local.pop('self') # prevent error of multiple value for args
        self.data = kwargs_local
        response = self.conn.post(urn, self.data)

        return IuguPlan(**response)

    def get(self):
        pass

    def get_by_identifier(self):
        pass

    def getitems(self):
        pass

    def set(self):
        pass

    def save(self):
        pass

    def remove(self):
        pass

class Price(object):

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
            key = "prices[{key_name}]".format(key_name=k)
            data.append((key, v))

        return data


class Feature(object):

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
        if self.name and self.identifier and self.value:
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
            key = "features[{key_name]".format(key_name=k)
            data.append((key, v))

        return data
