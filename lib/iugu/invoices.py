__author__ = 'horacioibrahim'


# python-iugu package modules
import merchant, config, base, errors

class IuguInvoice(base.IuguApi):

    """

    This class allows handling invoices. The invoice is used to customers to
    make payments.

    :attribute class data: is a descriptor that carries rules of API fields.
    Only fields not None or not Blank can be sent.
    :attribute status: Accept two option: draft and pending, but can be
    draft, pending, [paid and canceled (internal use)]
    :attribute logs: is instanced a dictionary like JSON
    :attribute bank_slip: is instanced a dictionary like JSON

      => http://iugu.com/referencias/api#faturas
    """

    __conn = base.IuguRequests()

    def __init__(self, item=None, **kwargs):
        super(IuguInvoice, self).__init__(**kwargs)
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
        self.bank_slip = kwargs.get("bank_slip") # TODO: create a class/object.
        self.logs = kwargs.get("logs") # TODO: create a class/object
        # TODO: descriptors (getter/setter) for items
        _items = kwargs.get("items")
        self.items = None

        if _items:
            # TODO: list comprehensions
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
        custom_data = kwargs.get("custom_data")

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

        if custom_data:
            data.extend(custom_data)

        self._data = data

    def data_del(self):
        del self._data

    data = property(data_get, data_set, data_del, "data property set/get/del")

    def create(self, draft=False, return_url=None, email=None, expired_url=None,
               notification_url=None, tax_cents=None, discount_cents=None,
               customer_id=None, ignore_due_email=False, subscription_id=None,
               credits=None, due_date=None, items=None, custom_variables=None):
        """
        Creates an invoice and returns owns class

        :param subscription_id: must be existent subscription from API
        :param customer_id: must be API customer_id (existent customer)
        :param items: must be item instance of merchant.Item()
        :para custom_variables: a dict {'key':'value'}

          => http://iugu.com/referencias/api#faturas
        """
        urn = "/v1/invoices"

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
                # items are required. If it not passed as args,
                # it must to exist at least in instance object
                items = self.items # "force" declaring locally
            else:
                raise errors.IuguInvoiceException(value="Required items is" \
                                            " empty.")

        if not email:
            if self.email:
                # email is required. If it not passed as args,
                # it must to exist at least in instance object
                email = self.email # "force" declaring locally
            else:
                raise errors.IuguInvoiceException(value="Required customer" \
                                    " email is empty.")

        if custom_variables:
            custom_data = self.custom_variables_list(custom_variables)
        # to declare all variables local before calling locals().copy()
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self.__conn.post(urn, self.data)
        invoice = IuguInvoice(**response)
        return invoice

    def set(self, invoice_id, email=None, due_date=None,
               return_url=None, expired_url=None, notification_url=None,
               tax_cents=None, discount_cents=None, customer_id=None,
               ignore_due_email=False, subscription_id=None, credits=None,
               items=None, custom_variables=None):
        """ Updates/changes a invoice that already exists

        :param custom_variables: a dict {'key', value}. If previously values
        exist the variable is edited rather is added

        IMPORTANT: Only invoices with status "draft" can be changed all fields
        otherwise (if status pending, cancel or paid) only the field logs
        can to change.
        """
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)

        if items is not None:
            assert isinstance(items, merchant.Item), "item must be instance of Item"

        if custom_variables:
            custom_data = self.custom_variables_list(custom_variables)
        # to declare all variables local before calling locals().copy()
        kwargs_local = locals().copy()
        kwargs_local.pop('self')
        self.data = kwargs_local
        response = self.__conn.put(urn, self.data)

        return IuguInvoice(**response)

    def save(self):
        """Save updating a invoice's instance. To add/change custom_variables
        keywords to use create() or set()

        IMPORTANT: Only invoices with status "draft" can be changed
        """
        self.data = self.__dict__
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=self.id)
        response = self.__conn.put(urn, self.data)

        return IuguInvoice(**response)

    @classmethod
    def get(self, invoice_id):
        """Gets one invoice with base in invoice_id and returns instance"""
        data = []
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.__conn.get(urn, data)

        return IuguInvoice(**response)

    @classmethod
    def getitems(self, limit=None, skip=None, created_at_from=None,
                 created_at_to=None, query=None, updated_since=None, sort=None,
                 customer_id=None):
        """
        Gets a list of invoices where the API default is limited 100. Returns
        a list of IuguInvoice

        :param limit: limits the number of invoices returned by API
        :param skip: skips a numbers of invoices where more recent insert
        ordering. Useful to pagination.
        :param query: filters based in value (case insensitive)
        :param sort: sorts based in field. Use minus signal to determine the
        direction DESC or ASC (e.g sort="-email"). IMPORTANT: not work by API
        :return: list of IuguInvoice instances
        """
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

        invoices = self.__conn.get(urn, data)
        #TODO: list comprehensions
        invoices_objects = []
        for invoice_item in invoices["items"]:
            obj_invoice = IuguInvoice(**invoice_item)
            invoices_objects.append(obj_invoice)

        return invoices_objects

    def remove(self, invoice_id=None):
        """
        Removes an invoice by id or instance and returns None
        """
        invoice_id = invoice_id if invoice_id else self.id
        if invoice_id is None:
            raise errors.IuguSubscriptionsException(value="ID (invoice_id) can't be empty")

        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.__conn.delete(urn, [])
        obj = IuguInvoice(**response)
        # TODO: list comprehensions ?
        if obj:
            for k, v in self.__dict__.items():
                self.__dict__[k] = None

    def cancel(self):
        """Cancels an instance of invoice and returns own invoice with status
        canceled"""
        urn = "/v1/invoices/{invoice_id}/cancel".format(invoice_id=self.id)

        # This below if to avoid a request because the API not allow this operation
        # but all API can to change theirs behaviors so to allow to cancel
        # invoices with status difference of "pending".
        # The approach without if also to raise exception with error from directly
        # API responses but here the focus is less requests.
        if self.status == "pending":
            response = self.__conn.put(urn, [])
            obj = IuguInvoice(**response)
        else:
            raise errors.IuguGeneralException(value="Cancel operation support only " \
                "invoices with status: pending.")

        return obj

    @classmethod
    def to_cancel(self, invoice_id):
        """Cancels an invoice with base in invoice ID and returns own
        invoice with status canceled

          => http://iugu.com/referencias/api#cancelar-uma-fatura
        """
        urn = "/v1/invoices/{invoice_id}/cancel".format(invoice_id=invoice_id)
        response = self.__conn.put(urn, [])
        obj = IuguInvoice(**response)

        return obj

    def refund(self):
        """Makes refund of an instance of invoice

          => http://iugu.com/referencias/api#reembolsar-uma-fatura
        """
        urn = "/v1/invoices/{invoice_id}/refund".format(invoice_id=self.id)

        # This below if to avoid a request because the API not allow this operation
        # but all API can to change theirs behaviors so to allow to refund
        # invoices with status difference of "paid".
        # The approach without if also to raise exception with error from directly
        # API responses but here the focus is less requests.
        if self.status == "paid":
            response = self.__conn.post(urn, [])
            obj = IuguInvoice(**response)
        else:
            raise errors.IuguGeneralException(value="Refund operation support only " \
                "invoices with status: paid.")

        return obj
