__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors, merchant

class IuguSubscription(base.IuguApi):

    """

    This class allows handling subscriptions an CRUD with create, get, set,
    save and remove plus add-ons as getitems, suspend, activate, change_plan,
    is_credit_based.

    :attribute class data: is a description it carries rules of data to API
    """

    _conn = base.IuguRequests()

    def __init__(self, **kwargs):
        super(IuguSubscription, self).__init__(**kwargs)
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
        self.recent_invoices = kwargs.get("recent_invoices") # only resume of invoice
        self.logs = kwargs.get("logs")
        self._type = kwargs.get("_type") # facilities to verify if credit_base or general

        if isinstance(self._subitems, list):
            for item in self._subitems:
                obj_item = merchant.Item(**item)
                self.subitems.append(obj_item)

    @staticmethod
    def is_credit_based(response):
        # Checks if HTTP response of API subscription is credit_based type
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
        self.custom_variables = kwargs.get("custom_data")
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

        if self.custom_variables: # TODO: to create test
            data.extend(self.custom_variables)

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
            data.append(("skip_charge", value_skip_charge))

        self._data = data

    @data.deleter
    def data(self):
        del self._data

    def create(self, customer_id, plan_identifier, expires_at=None,
               only_on_charge_success=False, subitems=None,
               custom_variables=None):
        """
        Creates new subscription

        :param customer_id: the ID of an existent customer
        :param plan_identifier: the identifier of a plan (it's not ID)
        :param expires_at: a string with expiration date and next charge (e.g
        "DD/MM/YYYY" or "31/12/2014")
        :param only_on_charge_success: creates the subscriptions if charged
        with success. It's supported if customer already have payment method
        inserted
        :param subitems: items of subscriptions

          => http://iugu.com/referencias/api#criar-uma-assinatura
        """
        urn = "/v1/subscriptions"
        if custom_variables:
            assert isinstance(custom_variables, dict), "Required a dict"
            custom_data = self.custom_variables_list(custom_variables)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.post(urn, self.data)
        return IuguSubscription(**response)

    def set(self, sid, plan_identifier=None, expires_at=None,
            subitems=None, suspended=None, skip_charge=None,
            custom_variables=None, customer_id=None):
        """
        Changes a subscriptions with based arguments and Returns modified
        subscription of type no credit_based.

        :param sid: ID of an existent subscriptions in API
        :param customer_id: ID of customer
        :param expires_at: expiration date and date of next charge
        :param subitems: subitems
        :param suspended: boolean to change status of subscription
        :param skip_charge: ignore charge. Bit explanation and obscure in API
        :param custom_variables: a dictionary {'key': 'value'}

        IMPORTANT 1: Removed parameter customer_id. Iugu's support (number 782)
        says that to change only customer_id isn't supported by API.
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        if custom_variables:
            assert isinstance(custom_variables, dict), "Required a dict"
            custom_data = self.custom_variables_list(custom_variables)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.put(urn, self.data)
        response["_type"] = "general"
        return IuguSubscription(**response)

    def save(self):
        """Saves an instance of subscription and return own class instance
        modified"""

        if self.id:
            sid = self.id
        else:
            raise errors.IuguSubscriptionsException(value="Save is support "\
                        "only to returned API object.")

        kwargs = {}
        # TODO: to improve this ineffective approach
        # Currently this check if the required set's parameters was passed
        # If changes occurs in set() to revise this k in if used to mount kwargs
        for k, v in self.__dict__.items():
            if v is not None:
                if  k == "plan_identifier" or \
                    k == "expires_at" or k == "subitems" or \
                    k == "suspended" or k == "skip_charge" or \
                                k == "custom_variables":
                    kwargs[k] = v
                    last_valid_k = k

                if isinstance(v, list) and len(v) == 0 and last_valid_k:
                    # solves problem with arguments of empty lists
                    del kwargs[last_valid_k]

        return self.set(sid, **kwargs)

    @classmethod
    def get(self, sid):
        """
        Fetch one subscription based in ID and returns one of two's types of
        subscriptions: credit_based or no credit_based

        :param sid: ID of an existent subscriptions in API
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        response = self._conn.get(urn, [])

        if self.is_credit_based(response):
            response["_type"] = "credit_based"
            return SubscriptionCreditsBased(**response)

        response["_type"] = "general"
        return IuguSubscription(**response)

    @classmethod
    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None,
                 customer_id=None):
        """
        Gets subscriptions by API default limited 100.
        """
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
            if self.is_credit_based(s):
                s["_type"] = "credit_based"
                obj_subscription = SubscriptionCreditsBased(**s)
            else:
                s["_type"] = "general"
                obj_subscription = IuguSubscription(**s)

            subscriptions_objs.append(obj_subscription)

        return subscriptions_objs

    def remove(self, sid=None):
        """
        Removes a subscription given id or instance

        :param sid: ID of an existent subscriptions in API
        """
        if not sid:
            if self.id:
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        self._conn.delete(urn, [])

    def suspend(self, sid=None):
        """
        Suspends an existent subscriptions

        :param sid: ID of an existent subscriptions in API
        """
        if not sid:
            if self.id:
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}/suspend".format(sid=sid)
        response = self._conn.post(urn, [])

        if self.is_credit_based(response):
            response["_type"] = "credit_based"
            return SubscriptionCreditsBased(**response)

        response["_type"] = "general"
        return IuguSubscription(**response)

    def activate(self, sid=None):
        """
        Activates an existent subscriptions

        :param sid: ID of an existent subscriptions in API

        NOTE: This option not work fine by API
        """
        if not sid:
            if self.id:
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}/activate".format(sid=sid)
        response = self._conn.post(urn, [])

        if self.is_credit_based(response):
            response["_type"] = "credit_based"
            return SubscriptionCreditsBased(**response)

        response["_type"] = "general"
        return IuguSubscription(**response)

    def change_plan(self, plan_identifier, sid=None):
        """
        Changes the plan for existent subscriptions

        :param sid: ID of an existent subscriptions in API
        :param plan_identifier: the identifier of a plan (it's not ID)
        """
        if not sid:
            if self.id:
                # short-circuit
                if "credits_based" in self.__dict__ and self.credits_based:
                    raise errors.\
                        IuguSubscriptionsException(value="Instance must be " \
                                        "object of IuguSubscriptionsException")
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}/change_plan/{plan_identifier}"\
                .format(sid=sid, plan_identifier=plan_identifier)
        response = self._conn.post(urn, [])

        if self.is_credit_based(response):
            response["_type"] = "credit_based"
            return SubscriptionCreditsBased(**response)

        response["_type"] = "general"
        return IuguSubscription(**response)


class SubscriptionCreditsBased(IuguSubscription):

    """

    This class make additional approaches for subscriptions based in credits.
    Addition methods as add_credits and remove_credits.

    :method create: it has parameters different of class extended
    :method set: it has parameters different of class extended

    """

    def __init__(self, **kwargs):
        super(SubscriptionCreditsBased, self).__init__(**kwargs)
        self.credits_based = True
        self.credits_cycle = kwargs.get("credits_cycle")
        self.credits_min = kwargs.get("credits_min")
        self.credits = kwargs.get("credits")

    def create(self, customer_id, credits_cycle, price_cents=None,
               credits_min=None, expires_at=None, only_on_charge_success=None,
               subitems=None, custom_variables=None):
        """
        Create a subscription based in credits and return the instance
        this class.

        :param: custom_variables: a dict {'key': 'value'}
        """

        if price_cents is None or price_cents <= 0:
            raise errors.IuguSubscriptionsException(value="price_cents must be " \
                                         "greater than 0")

        credits_based = self.credits_based

        if custom_variables:
            assert isinstance(custom_variables, dict), "Required a dict"
            custom_data = self.custom_variables_list(custom_variables)

        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        urn = "/v1/subscriptions"
        self.data = kwargs_local
        response = self._conn.post(urn, self.data)
        response["_type"] = "credit_based"
        return SubscriptionCreditsBased(**response)

    def set(self, sid, expires_at=None, subitems=None, suspended=None,
            skip_charge=None, price_cents=None, credits_cycle=None,
            credits_min=None, custom_variables=None):
        """
        Changes an existent subscription no credit_based

        :param sid: ID of an existent subscriptions in API
        """
        urn = "/v1/subscriptions/{sid}".format(sid=sid)
        credits_based = self.credits_based
        if custom_variables:
            assert isinstance(custom_variables, dict), "Required a dict"
            custom_data = self.custom_variables_list(custom_variables)
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self._conn.put(urn, self.data)
        response["_type"] = "credit_based"
        return SubscriptionCreditsBased(**response)

    def save(self):
        """ Saves an instance of this class that was persisted or raise error
         if no instance.

        NOTE: to use create() or set() for add/change custom_variables
        """
        if self.id:
            sid = self.id
        else:
            raise errors.IuguSubscriptionsException(value="Save is support "\
                        "only to returned API object.")

        kwargs = {}
        # TODO: to improve this ineffective approach.
        # Currently this check if the set's parameters was passed. If changes
        # occurs in set() to revise this k in if used to mount kwargs
        for k, v in self.__dict__.items():
            if v is not None:
                if  k == "expires_at" or \
                    k == "subitems" or k == "suspended" or \
                    k == "skip_charge" or k == "price_cents" or \
                    k == "credits_cycle" or k == "credits_min" or \
                    k == "custom_variables" :
                    kwargs[k] = v
                    last_valid_k = k

                    if isinstance(v, list) and len(v) == 0 and last_valid_k:
                        # solves problem with arguments of empty lists
                        del kwargs[last_valid_k]
                        del last_valid_k

        return self.set(sid, **kwargs)

    def add_credits(self, quantity, sid=None):
        """
        Adds credits in existent subscriptions

        :param sid: ID of an existent subscriptions in API
        :param plan_identifier: the identifier of a plan (it's not ID)
        """
        data = []
        if not sid:
            if self.id:
                if not self.credits_based:
                    raise errors.\
                        IuguSubscriptionsException(value="Instance must be " \
                                        "object of SubscriptionCreditsBased")
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}/add_credits".format(sid=sid)
        data.append(("quantity", quantity))
        response = self._conn.put(urn, data)

        if not self.is_credit_based(response):
            raise errors.IuguSubscriptionsException(value="Instance must be " \
                                        "object of SubscriptionCreditsBased")

        response["_type"] = "credit_based"
        return SubscriptionCreditsBased(**response)

    def remove_credits(self, quantity, sid=None):
        """
        Suspends an existent subscriptions

        :param sid: ID of an existent subscriptions in API
        :param plan_identifier: the identifier of a plan (it's not ID)
        """
        data = []
        if not sid:
            if self.id:
                if not self.credits_based:
                    raise errors.\
                        IuguSubscriptionsException(value="Instance must be " \
                                        "object of SubscriptionCreditsBased")
                sid = self.id
            else:
                raise errors.IuguSubscriptionsException(value="ID (sid) can't be empty")

        urn = "/v1/subscriptions/{sid}/remove_credits".format(sid=sid)
        data.append(("quantity", quantity))
        response = self._conn.put(urn, data)

        if not self.is_credit_based(response):
            raise errors.IuguSubscriptionsException(value="Instance must be " \
                                        "object of SubscriptionCreditsBased")

        response["_type"] = "credit_based"
        return SubscriptionCreditsBased(**response)
