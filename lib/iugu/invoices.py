__author__ = 'horacioibrahim'


# python-iugu package modules
import merchant, config, base, errors

class IuguInvoice(object):

    API_TOKEN = config.API_TOKEN
    conn = base.IuguRequests()

    def __init__(self, item=None, **kwargs):
        self.id = kwargs.get("id")
        self.due_date = kwargs.get("due_date")
        self.currency = kwargs.get("currency")
        self.discount_cents = kwargs.get("discount_cents")
        # self.customer_email = kwargs.get("customer_email")
        self.email = kwargs.get("email") # customer email
        self.items_total_cents = kwargs.get("items_total_cents")
        self.notification_url = kwargs.get("notification_url")
        self.return_url = kwargs.get("return_url")
        self.status = kwargs.get("status") # [draft,pending] internal:[paid,canceled]
        self.expiration_url = kwargs.get("expiration_url")
        self.tax_cents = kwargs.get("tax_cents")
        self.updated_at = kwargs.get("updated_at")
        self.total_cents = kwargs.get("total_cents")
        self.paid_at = kwargs.get("paid_at")
        self.secure_id = kwargs.get("secure_id")
        self.secure_url = kwargs.get("secure_url")
        self.customer_id = kwargs.get("customer_id")
        self.user_id = kwargs.get("user_id")
        self.total = kwargs.get("total")
        self.created_at = kwargs.get("created_at")
        self.taxes_paid = kwargs.get("taxes_paid")
        self.interest = kwargs.get("interest")
        self.discount = kwargs.get("discount")
        self.refundable = kwargs.get("refundable")
        self.installments = kwargs.get("installments")
        self.blank_slip = kwargs.get("blank_slip") # TODO: create a class/object.
        self.logs = kwargs.get("logs") # TODO: create a class/object
        # TODO: descriptors (getter/setter) for items
        _items = kwargs.get("items")
        self.items = None

        if _items:
            _list_items = []
            for i in _items:
                obj_item = merchant.Item(**i)
                _list_items.append(obj_item)
            self.items = _list_items
        else:
            if item:
                assert isinstance(item, merchant.Item), "item must be instance of Item"
                self.items = item


        self.variables = kwargs.get("variables")
        self.logs = kwargs.get("logs")
        self.custom_variables = kwargs.get("custom_variables")
        self._data = None

    # constructor of data descriptors
    def data_get(self):
        return self._data

    def data_set(self, kwargs):
        draft = kwargs.get("draft")
        return_url = kwargs.get("return_url")
        expired_url = kwargs.get("expired_url")
        notification_url = kwargs.get("notification_url")
        tax_cents = kwargs.get("tax_cents")
        discount_cents = kwargs.get("discount_cents")
        customer_id = kwargs.get("customer_id")
        ignore_due_email = kwargs.get("ignore_due_email")
        subscription_id = kwargs.get("subscription_id")
        due_date = kwargs.get("due_date")
        credits = kwargs.get("credits")
        items = kwargs.get("items")
        email = kwargs.get("email")

        data = []

        if draft:
            data.append(("status", "draft")) # default is pending

        # data will posted and can't null, None or blank
        if return_url:
            self.return_url = return_url

        if self.return_url:
            data.append(("return_url", self.return_url))

        if expired_url:
            self.expiration_url = expired_url

        if self.expiration_url:
            data.append(("expired_url", self.expiration_url))

        if notification_url:
            self.notification_url = notification_url

        if self.notification_url:
            data.append(("notification_url", self.notification_url))

        if tax_cents:
            self.tax_cents = tax_cents

        data.append(("tax_cents", self.tax_cents))

        if discount_cents:
            self.discount_cents = discount_cents

        data.append(("discount_cents", self.discount_cents))

        if customer_id:
            self.customer_id = customer_id

        if self.customer_id:
            data.append(("customer_id", self.customer_id))

        if credits:
            data.append(("credits", credits))

        if ignore_due_email:
            data.append(("ignore_due_email", True))

        if subscription_id:
            data.append(("subscription_id", subscription_id))

        if due_date:
            self.due_date = due_date

        if self.due_date:
            data.append(("due_date", self.due_date))

        if isinstance(items, list):
            for item in items:
                data.extend(item.to_data())
        else:
            if items is not None:
                data.extend(items.to_data())

        if email:
            self.email = email

        if self.email:
            data.append(("email", self.email))

        self._data = data

    def data_del(self):
        del self._data

    data = property(data_get, data_set, data_del, "data property set/get/del")

    def create(self, draft=False, return_url=None, email=None, expired_url=None,
               notification_url=None, tax_cents=None, discount_cents=None,
               customer_id=None, ignore_due_email=False, subscription_id=None,
               credits=None, due_date=None, items=None):
        """
        Creates an invoice

        :param subscription_id: must be existent subscription from API
        :param customer_id: must be API customer_id (existent customer)
        :param items: must be item instance

        TODO: to support logs and custom_variables

          => http://iugu.com/referencias/api#faturas
        """

        # handling required fields
        if not due_date:
            if self.due_date:
                # due_date is required. If it not passed in args, it must to
                # exist at least in instance object
                due_date = self.due_date # "force" declaring locally
            else:
                raise errors.IuguInvoiceException(value="Required due_date is" \
                                                " empty.")

        if not items:
            if self.items:
                # At create items is required. If it not passed as args,
                # it must to exist at least in instance object
                items = self.items # "force" declaring locally
            else:
                raise errors.IuguInvoiceException(value="Required items is" \
                                            " empty.")

        if not email:
            if self.email:
                # At create email is required. If it not passed as args,
                # it must to exist at least in instance object
                email = self.email # "force" declaring locally
            else:
                raise errors.IuguInvoiceException(value="Required customer" \
                                    " email is empty.")

        # to declare all variables local before locals().copy()
        kwargs_local = locals().copy()
        kwargs_local.pop('self')

        #if self.email is None or self.due_date is None or \
             #   self.items is None:
           # raise errors.IuguInvoiceException

        self.data = kwargs_local

        urn = "/v1/invoices"
        response = self.conn.post(urn, self.data)
        invoice = IuguInvoice(item=self.items, **response) # TODO: review item arg if required
        return invoice

    @classmethod
    def get(self, invoice_id):
        data = []
        # data.append(("api_token", self.API_TOKEN))
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.conn.get(urn, data)

        return IuguInvoice(**response)

    @classmethod
    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None,
                 customer_id=None):
        data = []
        urn = "/v1/invoices/"

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

        invoices = self.conn.get(urn, data)
        invoices_objects = []
        for invoice_item in invoices["items"]:
            obj_invoice = IuguInvoice(**invoice_item)
            invoices_objects.append(obj_invoice)

        return invoices_objects

    def set(self, invoice_id, email=None, due_date=None,
               return_url=None, expired_url=None, notification_url=None,
               tax_cents=None, discount_cents=None, customer_id=None,
               ignore_due_email=False, subscription_id=None, credits=None,
               items=None):

        if items is not None:
            assert isinstance(items, merchant.Item), "item must be instance of Item"

        # to declare all variables local before locals().copy()
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        changes_count = len([ k for k, v in kwargs_local.items() if v is not None])

        if changes_count < 3:
            raise errors.IuguInvoiceException(value="At least one field is "\
                "required to edit/change")

        self.data = kwargs_local


        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.conn.put(urn, self.data)

        return IuguInvoice(**response)

    def save(self):

        self.data = self.__dict__
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=self.id)
        response = self.conn.put(urn, self.data)

        return IuguInvoice(**response)

    def remove(self):
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=self.id)
        response = self.conn.delete(urn, [])
        obj = IuguInvoice(**response)
        if obj:
            for k, v in self.__dict__.items():
                self.__dict__[k] = None

    def cancel(self):
        urn = "/v1/invoices/{invoice_id}/cancel".format(invoice_id=self.id)
        if self.status == "pending":
            response = self.conn.put(urn, [])
            obj = IuguInvoice(**response)
        else:
            raise errors.IuguGeneralException(value="Cancel operation support only " \
                "invoices with status: pending.")

        return obj

    @classmethod
    def to_cancel(self, invoice_id):
        urn = "/v1/invoices/{invoice_id}/cancel".format(invoice_id=invoice_id)
        response = self.conn.put(urn, [])
        obj = IuguInvoice(**response)

        return obj

    def refund(self):
        urn = "/v1/invoices/{invoice_id}/refund".format(invoice_id=self.id)
        if self.status == "paid":
            response = self.conn.post(urn, [])
            obj = IuguInvoice(**response)
        else:
            raise errors.IuguGeneralException(value="Refund operation support only " \
                "invoices with status: paid.")

        return obj






