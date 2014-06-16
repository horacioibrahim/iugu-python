# coding: utf-8

class IuguPaymentMethodException(BaseException):

    def __init__(self, value="Required customer_id must not be blank or None"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IuguGeneralException(BaseException):

    def __init__(self, value="Data returned not matches with iugu-python classes"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IuguInvoiceException(BaseException):

    def __init__(self, value="Incomplete request for create invoices"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IuguPlansException(BaseException):

    def __init__(self, value="Incomplete request for create plans"):
        self.value = value

    def __str__(self):
        return repr(self.value)
