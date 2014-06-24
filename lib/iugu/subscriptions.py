__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors, merchant

class IuguSubscriptions(base.IuguApi):

    _conn = base.IuguRequests()

    def __init__(self, **kwargs):
        super(IuguSubscriptions, self).__init__(**kwargs)
        self.id = kwargs.get("id")
        # required
        self.customer_id = kwargs.get("customer_id")
        # optionals
        self.plan_identifier = kwargs.get("plan_identifier") # only credits_based subscriptions
        self.expires_at = kwargs.get("expires_at")
        # self.only_on_charge_success = kwargs.get("only_on_charge_success") # if exist payment method for client
        self._subitems = kwargs.get("subitems")
        self.subitems = [] # of items
        self.custom_variables = kwargs.get("custom_variables")
        self._data = None
        self.suspended = kwargs.get("suspended")
        self.price_cents = kwargs.get("price_cents")
        self.currency = kwargs.get("currency")
        # created by api
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.customer_name = kwargs.get("customer_name")
        self.customer_email = kwargs.get("customer_email")
        self.cycled_at = kwargs.get("cycled_at")
        self.plan_name = kwargs.get("plan_name")
        self.customer_ref = kwargs.get("customer_ref")
        self.plan_ref = kwargs.get("plan_ref")
        self.active = kwargs.get("active")
        self.in_trial = kwargs.get("in_trial")
        self.recent_invoices = kwargs.get("recent_invoices")
        self.logs = kwargs.get("logs")

        if isinstance(self._subitems, list):
            for item in self._subitems:
                obj_item = merchant.Item(**item)
                self.subitems.append(obj_item)

    @staticmethod
    def is_credit_based(response):
        # Checks if subscription is credit_based type
        if "credits_based" in response and response["credits_based"] == True:
            return True
        return False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, kwargs):
        """
        Body data for request send
        """
        data = []
        self.id = kwargs.get("sid")
        self.customer_id = kwargs.get("customer_id")
        self.plan_identifier = kwargs.get("plan_identifier")
        self.expires_at = kwargs.get("expires_at")
        self.only_on_charge_success = kwargs.get("only_on_charge_success")
        self.subitems = kwargs.get("subitems")
        self.custom_variables = kwargs.get("custom_variables")
        self.credits_based = kwargs.get("credits_based")
        self.credits_min = kwargs.get("credits_min")
        self.credits_cycle = kwargs.get("credits_cycle")
        self.price_cents = kwargs.get("price_cents")
        self.suspended = kwargs.get("suspended")
        self.skip_charge = kwargs.get("skip_charge")

        if self.id:
            data.append(("id", self.id))

        if self.customer_id:
            data.append(("customer_id", self.customer_id))

        if self.plan_identifier:
            data.append(("plan_identifier", self.plan_identifier))

        if self.expires_at:
            data.append(("expires_at", self.expires_at))

        if self.only_on_charge_success:
            value_charge_success = str(self.only_on_charge_success)
            value_charge_success = value_charge_success.lower()
            data.append(("only_on_charge_success", value_charge_success))

        if self.subitems:
            if isinstance(self.subitems, list):
                for item in self.subitems:
                    data.extend((item.to_data(is_subscription=True)))
            else:
                raise errors.IuguSubscriptionsException("The subitems must be " \
                    "a list of obj Item")

        if self.custom_variables:
            pass

        # credit based subscriptions
        if self.credits_based is not None:
            value_credits_based = str(self.credits_based)
            value_credits_based = value_credits_based.lower()
            data.append(("credits_based", value_credits_based))

        if self.credits_min:
            data.append(("credits_min", self.credits_min))

        if self.credits_cycle:
            data.append(("credits_cycle", self.credits_cycle))

        if self.price_cents:
            data.append(("price_cents", self.price_cents))

        if self.suspended is not None:
            value_suspended = str(self.suspended)
            value_suspended = value_suspended.lower()
            data.append(("suspended", value_suspended))

        if self.skip_charge is not None:
            value_skip_charge = str(self.skip_charge)
            value_skip_charge = value_skip_charge.lower()
            data.append(("suspended", value_skip_charge))

        self._data = data

    @data.deleter
    def data(self):
        del self._data

    def create(self, customer_id, plan_identifier, expires_at=None,
               only_on_charge_success=False, subitems=None, custom_variables=None):
        """
        Creates new subscription
        """
        urn = "/v1/subscriptions"
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.post(urn, self.data)
        return IuguSubscriptions(**response)

    @classmethod
    def get(self, sid):
        """
        Fetch one subscription based in ID and returns one of two's types of
        subscriptions: credit_based or no credit_based
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        response = self._conn.get(urn, [])

        if self.is_credit_based(response):
            return SubscriptionCreditsBased(**response)

        return IuguSubscriptions(**response)

    @classmethod
    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None,
                 customer_id=None):

        data = []
        urn = "/v1/subscriptions/"

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
        if customer_id:
            data.append(("customer_id", customer_id))

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

        subscriptions = self._conn.get(urn, data)
        subscriptions_objs = []
        for s in subscriptions["items"]:
            # add items in list but before verifies if credit_based
            if IuguSubscriptions.is_credit_based(s):
                obj_subscription = SubscriptionCreditsBased(**s)
            else:
                obj_subscription = IuguSubscriptions(**s)

            subscriptions_objs.append(obj_subscription)

        return subscriptions_objs

    def set(self, sid, customer_id=None, plan_identifier=None, expires_at=None,
            only_on_charge_success=False, subitems=None, custom_variables=None,
            suspended=False, skip_charge=False):
        """
        Changes an existent subscription no credit_based
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.put(urn, self.data)
        return IuguSubscriptions(**response)

    def save(self):
        sid = self.id
        kwargs = {}

        # TODO ineffective approach
        for k, v in self.__dict__.items():
            if k == "customer_id" or k == "plan_identifier" or k == "expires_at" \
                or k == "only_on_charge_success" or k == "subitems" or \
                k == "custom_variables":
                kwargs[k] = v

        return self.set(sid, **kwargs)

    def remove(self, sid=None):
        """
        Removes a subscription given id or instance
        """
        if not sid:
            if self.id:
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID can't be empty")

        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        self._conn.delete(urn, [])


class SubscriptionCreditsBased(IuguSubscriptions):

    def __init__(self, **kwargs):
        super(SubscriptionCreditsBased, self).__init__(**kwargs)
        self.credits_based = True
        self.credits_cycle = kwargs.get("credits_cycle")
        self.credits_min = kwargs.get("credits_min")
        self.credits = kwargs.get("credits")

    def create(self, customer_id, credits_cycle, price_cents=None,
               credits_min=None, expires_at=None, only_on_charge_success=None,
               subitems=None, custom_variables=None):

        if price_cents is None or price_cents <= 0:
            raise errors.IuguSubscriptionsException(value="price_cents must be " \
                                         "greater than 0")
        credits_based = self.credits_based

        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        urn = "/v1/subscriptions"
        self.data = kwargs_local
        print self.data
        response = self._conn.post(urn, self.data)
        return SubscriptionCreditsBased(**response)

    def set(self, sid, customer_id=None, plan_identifier=None, expires_at=None,
            only_on_charge_success=False, subitems=None, custom_variables=None,
            suspended=False, skip_charge=False, price_cents=None,
            credits_cycle=None, credits_min=None):
        """
        Changes an existent subscription no credit_based
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.put(urn, self.data)
        return SubscriptionCreditsBased(**response)
