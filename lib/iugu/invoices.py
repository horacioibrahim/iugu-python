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
        self.customer_email = kwargs.get("customer_email")
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
        _items = kwargs.get("items")

        if _items:
            _list_items = []
            for i in _items:
                obj_item = merchant.Item(**i)
                _list_items.append(obj_item)
            self.items = _list_items
        else:
            assert isinstance(item, merchant.Item), "item must be instance of Item"
            self.items = item

        self.variables = kwargs.get("variables")
        self.logs = kwargs.get("logs")
        self.custom_variables = kwargs.get("custom_variables")

    def create(self, status=False):
        data = []

        if self.customer_email is None or self.due_date is None or \
                self.items is None:
            raise errors.IuguInvoiceException

        if status:
            data.append(("status", "draft")) # default is pending

        data.append(("api_token", self.API_TOKEN))
        data.append(("email", self.customer_email)) # customer email of Store
        data.append(("due_date", self.due_date))

        if isinstance(self.items, list):
            for item in self.items:
                data.extend(item.to_data())
        else:
            data.extend(self.items.to_data())

        urn = "/v1/invoices"
        response = self.conn.post(urn, data)
        invoice = IuguInvoice(customer_email=self.customer_email,
                              item=self.items, **response)
        return invoice

    @classmethod
    def get(self, invoice_id):
        data = []
        data.append(("api_token", self.API_TOKEN))
        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.conn.get(urn, data)

        return IuguInvoice(**response)

    @classmethod
    def set(self, invoice_id=None, due_date=None, customer_email=None, **kwargs):
        data = []
        data.append(("api_token", self.API_TOKEN))

        for k, v in kwargs.items():
            data.append((k, v))

        urn = "/v1/invoices/{invoice_id}".format(invoice_id=invoice_id)
        response = self.conn.put(urn, data)
        print response





