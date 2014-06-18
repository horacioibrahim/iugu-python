__author__ = 'horacioibrahim'

# python-iugu package modules
import base, config, errors, merchant

class IuguSubscriptions(base.IuguApi):

    conn = base.IuguRequests()

    def __init__(self, **kwargs):
        super(IuguSubscriptions, self).__init__(**kwargs)
        # required
        self.customer_id = kwargs.get("customer_id")
        # optionals
        self.plan_identifier = kwargs.get("plan_identifier") # only credits_based subscriptions
        self.expires_at = kwargs.get("expires_at")
        self.only_on_charge_success = kwargs.get("only_on_charge_success") # if exist payment method for client
        self._subitems = kwargs.get("subitems")
        self.subitems = [] # of items
        self.custom_variables = kwargs.get("custom_variables")
        self._data = None
        if isinstance(self._subitems, list):
            for item in self._subitems:
                obj_item = merchant.Item(**item)
                self.subitems.append(obj_item)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, kwargs):
        """
        Body data for request send
        """
        data = []
        self.customer_id = kwargs.get("customer_id")
        self.plan_identifier = kwargs.get("plan_identifier")
        self.expires_at = kwargs.get("expires_at")
        self.only_on_charge_success = kwargs.get("only_on_charge_success")
        self.subitems = kwargs.get("subitems")
        self.custom_variables = kwargs.get("custom_variables")

        if self.customer_id:
            data.append(("customer_id", self.customer_id))

        if self.plan_identifier:
            data.append(("plan_identifier", self.plan_identifier))

        if self.expires_at:
            data.append(("expires_at", self.expires_at))

        if self.only_on_charge_success:
            data.append(("only_on_charge_success", self.only_on_charge_success))

        if self.subitems:
            if isinstance(self.subitems, list):
                for item in self.subitems:
                    data.extend((item.to_data(is_subscription=True)))
            else:
                raise errors.IuguSubscriptionsException("The subitems must be " \
                    "a list of obj Item")

        if self.custom_variables:
            pass


    @data.deleter
    def data(self):
        del self._data

    def create(self, customer_id, plan_identifier, expires_at=None,
               only_on_charge_success=None, subitems=None, custom_variables=None):
        pass




class SubscriptionCreditsBased(IuguSubscriptions):

    def __init__(self, **kwargs):
        super(SubscriptionCreditsBased, self).__init__(**kwargs)
        self.credits_based = kwargs.get("credits_based")
        self.price_cents = kwargs.get("price_cents")
        self.credits_cycle = kwargs.get("credits_cycle")
        self.credits_min = kwargs.get("credits_min")


    def create(self, customer_id, credits_based=None, credits_cycle=None,
               expires_at=None, only_on_charge_success=None, subitems=None,
               custom_variables=None):
        pass