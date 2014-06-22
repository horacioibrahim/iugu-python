#coding: utf-8

__author__ = 'horacioibrahim'

import unittest
from time import sleep, ctime, time
from random import randint
from hashlib import md5
from types import StringType

# python-iugu package modules
import merchant, customers, config, invoices, errors, plans, subscriptions


class TestMerchant(unittest.TestCase):

    # TODO: remove charges created

    def setUp(self):
        self.API_TOKEN_TEST = config.API_TOKEN_TEST
        self.EMAIL_CUSTOMER  = config.ACCOUNT_EMAIL
        self.client = merchant.IuguMerchant(account_id=config.ACCOUNT_ID,
                                       api_mode_test=True,
                                       api_token=self.API_TOKEN_TEST)

    def test_create_payment_token_is_test(self):
        response = self.client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        self.assertTrue(response.is_test)

    def test_create_payment_token(self):
        response = self.client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        self.assertEqual(response.status, 200)

    def test_create_charge_credit_card(self):
        item = merchant.Item("Produto My Test", 1, 10000)
        token = self.client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        charge = self.client.create_charge(self.EMAIL_CUSTOMER, item, token=token.id)
        self.assertEqual(charge.is_success(), True)

    def test_create_charge_blank_slip(self):
        item = merchant.Item("Produto Blank Slip", 1, 1000)
        charge = self.client.create_charge(self.EMAIL_CUSTOMER, item)
        self.assertEqual(charge.is_success(), True)


class TestCustomer(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.random_user_email = email


    def test_create_customer_basic_info(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        c = consumer.create()
        c.remove()
        self.assertEqual(consumer.email, c.email)

    def test_create_customer_basic_email(self):
        consumer = customers.IuguCustomer()
        c = consumer.create(email=self.random_user_email)
        c.remove()
        self.assertEqual(consumer.email, c.email)

    def test_create_customer_extra_attrs(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        c = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        c.remove()
        self.assertEqual(consumer.email, c.email)

    def test_get_customer(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        consumer_new = consumer.create()
        c = consumer.get(customer_id=consumer_new.id)
        consumer_new.remove()
        self.assertEqual(consumer.email, c.email)

    def test_set_customer(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        c = consumer.set(consumer_new.id, name="Lago Mario")
        consumer_new.remove()
        self.assertEqual(c.name, "Lago Mario")

    def test_customer_save(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])

        # Edit info
        consumer_new.name = "Ibrahim Horacio"
        # Save as instance
        consumer_new.save()
        # verify results
        check_user = consumer.get(consumer_new.id)
        consumer_new.remove()
        self.assertEqual(check_user.name, "Ibrahim Horacio")

    def test_customer_delete_by_id(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        consumer.delete(consumer_new.id)
        self.assertRaises(errors.IuguGeneralException, consumer.get,
                                consumer_new.id)

    def test_customer_delete_instance(self):
        consumer = customers.IuguCustomer(api_mode_test=True,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])

        r = consumer_new.remove()
        self.assertRaises(errors.IuguGeneralException, consumer.get,
                                consumer_new.id)


class TestCustomerLists(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.API_TOKEN_TEST = config.API_TOKEN_TEST
        self.random_user_email = email

        self.c = customers.IuguCustomer(api_mode_test=True,
                                  api_token=self.API_TOKEN_TEST,
                                  email=self.random_user_email)

        # creating customers for tests with lists
        p1, p2, p3 = "Andrea", "Bruna", "Carol"
        self.one = self.c.create(name=p1, notes="It's the man",
                                     custom_variables=["local", "cup"])

        # I'm not happy with it (sleep), but was need. This certainly occurs because
        # time data is not a timestamp.
        sleep(1)
        self.two = self.c.create(name=p2, notes="It's the man",
                                     custom_variables=["local", "cup"])
        sleep(1)
        self.three = self.c.create(name=p3, notes="It's the man",
                                     custom_variables=["local", "cup"])
        sleep(1)

        self.p1, self.p2, self.p3 = p1, p2, p3

    def tearDown(self):
        self.one.remove()
        self.two.remove()
        self.three.remove()

    def test_getitems(self):
        customers_list = self.c.getitems()
        self.assertEqual(type(customers_list), list)

    def test_getitems_limit(self):
        # get items with auto DESC order
        customers_list = self.c.getitems(limit=2)
        self.assertEqual(len(customers_list), 2)

    def test_getitems_start(self):
        # get items with auto DESC order
        sleep(2)
        customers_list = self.c.getitems(limit=3) # get latest three customers
        reference_customer = customers_list[2].name
        customers_list = self.c.getitems(skip=2)
        self.assertEqual(customers_list[0].name, reference_customer)

    def test_getitems_query_by_match_in_name(self):
        hmd5 = md5()
        hmd5.update(ctime(time()))
        salt = hmd5.hexdigest()
        term = 'name_inexistent_or_improbable_here_{salt}'.format(salt=salt)

        # test value/term in >>name<<
        customer = self.c.create(name=term)
        sleep(2)
        items = self.c.getitems(query=term) # assert valid because name
        customer.remove()
        self.assertEqual(items[0].name, term)

    def test_getitems_query_by_match_in_notes(self):
        hmd5 = md5()
        hmd5.update(ctime(time()))
        salt = hmd5.hexdigest()
        term = 'name_inexistent_or_improbable_here_{salt}'.format(salt=salt)
        # test value/term in >>notes<<
        customer = self.c.create(name="Sub Zero", notes=term)
        sleep(2)
        items = self.c.getitems(query=term)
        customer.remove()
        self.assertEqual(items[0].notes, term)

    def test_getitems_query_by_match_in_email(self):
        hmd5 = md5()
        hmd5.update(ctime(time()))
        salt = hmd5.hexdigest()
        term = 'name_inexistent_or_improbable_here_{salt}'.format(salt=salt)
        # test value/term in >>email<<
        email = term + '@email.com'
        self.c.email = email
        customer = self.c.create()
        sleep(2)
        items = self.c.getitems(query=term)
        customer.remove()
        self.assertIn(term, items[0].email)

    # Uncomment/comment the next one line to disable/enable the test
    @unittest.skip("Database of webservice is not empty")
    def test_getitems_sort(self):
        sleep(1) # Again. It's need
        # Useful to test database with empty data (previous data, old tests)
        customers_list = self.c.getitems(sort="name")

        # monkey skip
        if len(customers_list) < 4:
            self.assertEqual(customers_list[0].name, self.p1)
        else:
            raise TypeError("API Database is not empty. This test isn't useful. " \
                "Use unittest.skip() before this method.")

    def test_getitems_created_at_from(self):
        sleep(1)
        customers_list = self.c.getitems(created_at_from=self.three.created_at)
        self.assertEqual(customers_list[0].id, self.three.id)

    # Uncomment the next one line to disable the test
    # @unittest.skip("Real-time interval not reached")
    def test_getitems_created_at_to(self):
        sleep(1)
        customers_list = self.c.getitems(created_at_to=self.one.created_at)
        self.assertEqual(customers_list[0].id, self.three.id)

    def test_getitems_updated_since(self):
        # get items with auto DESC order
        sleep(1)
        customers_list = self.c.getitems(updated_since=self.three.created_at)
        self.assertEqual(customers_list[0].id, self.three.id)


class TestCustomerPayments(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.API_TOKEN_TEST = config.API_TOKEN_TEST
        self.random_user_email = email
        self.client = customers.IuguCustomer(email="test@testmail.com")
        self.customer = self.client.create()

        self.instance_payment = self.customer.payment.create(description="New payment method",
                             number='4111111111111111',
                             verification_value=123,
                             first_name="Joao", last_name="Maria",
                             month=12, year=2014)

    def tearDown(self):
        self.instance_payment.remove()
        self.customer.remove() # if you remove customer also get payment

    def test_create_payment_method_new_user_by_create(self):
        """ Test create payment method to new recent user returned by create()
        of IuguCustomer
        """
        instance_payment = self.customer.payment.create(description="New payment method",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="Joao", last_name="Maria",
                                     month=12, year=2014)
        instance_payment.remove()
        self.assertTrue(isinstance(instance_payment, customers.IuguPaymentMethod))

    def test_create_payment_method_existent_user_by_get(self):
        """ Test create payment method of existent user returned by get()
        of IuguCustomer.
        """
        new_customer = self.client.create()
        # Test with user from get()
        existent_customer = self.client.get(new_customer.id)

        instance_payment = existent_customer.payment.create(description="New payment method",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="Joao", last_name="Maria",
                                     month=12, year=2015)
        instance_payment.remove()
        self.assertTrue(isinstance(instance_payment, customers.IuguPaymentMethod))

    def test_create_payment_method_existent_user_by_getitems(self):
        """ Test create payment method of existent user returned by getitems()
        of IuguCustomer
        """
        # Test with user from getitems()
        customers = self.client.getitems()
        c_0 = customers[0]
        instance_payment = c_0.payment.create(description="New payment method",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="Joao", last_name="Maria",
                                     month=12, year=2016)
        instance_payment.remove()
        self.assertTrue(isinstance(instance_payment, customers.IuguPaymentMethod))

    def test_create_payment_method_non_existent_user_by_instance(self):
        """ Test create payment method to instance's user before it was
        created in API. So without ID.
        """
        create = self.client.payment.create

        self.assertRaises(errors.IuguPaymentMethodException,
                          create, description="New payment method",
                          number='4111111111111111',
                          verification_value=123, first_name="Joao",
                          last_name="Maria", month=12, year=2016)

    def test_create_payment_method_raise_general(self):
        # Create payment method without data{} where API returns error.
        customer = self.client.create()
        self.assertRaises(errors.IuguGeneralException, customer.payment.create,
                          description="Second payment method")
        customer.remove()

    def test_get_payment_method_by_payment_id_customer_id(self):
        # Test get payment based payment_id and customer_id
        id = self.instance_payment.id
        # two args passed
        payment = self.client.payment.get(id, customer_id=self.customer.id)
        self.assertTrue(isinstance(payment, customers.IuguPaymentMethod))

    def test_get_payment_by_customer(self):
        # Test get payment by instance's customer (existent in API)
        id = self.instance_payment.id
        # one arg passed. user is implicit to customer
        payment = self.customer.payment.get(id)
        self.assertTrue(isinstance(payment, customers.IuguPaymentMethod))

    def test_set_payment_by_payment_id_customer_id(self):
        # Changes payment method base payment_id and customer_id
        id = self.instance_payment.id
        # two args passed
        payment = self.client.payment.set(id, "New Card Name",
                                          customer_id=self.customer.id)
        self.assertTrue(isinstance(payment, customers.IuguPaymentMethod))
        payment_test = self.customer.payment.get(payment.id)
        self.assertEqual(payment_test.description, payment.description)

    def test_set_payment_by_customer(self):
        # Changes payment method base payment_id of an intance's customer
        id = self.instance_payment.id
        # one arg passed. user is implicit to customer
        payment = self.customer.payment.set(id, "New Card Name")
        self.assertTrue(isinstance(payment, customers.IuguPaymentMethod))
        payment_test = self.customer.payment.get(payment.id)
        self.assertEqual(payment_test.description, payment.description)

    def test_set_payment_by_customer_by_save(self):
        """ Changes payment method of an instance's payment no payment_id or
        no customer_id is need"""
        self.instance_payment.description = "New Card Name"
        # no args passed. To payment method instance this is implicit
        payment = self.instance_payment.save()
        self.assertTrue(isinstance(payment, customers.IuguPaymentMethod))
        payment_test = self.customer.payment.get(payment.id)
        self.assertEqual(payment_test.description, payment.description)

    def test_set_payment_remove(self):
        """ Changes payment method of an instance's payment no payment_id or
        no customer_id is need"""
        instance_payment = self.customer.payment.create(description="New payment method",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="Joao", last_name="Maria",
                                     month=12, year=2014)
        instance_payment.remove()
        # Try get payment already removed
        payment_test = self.customer.payment.get # copy method
        self.assertRaises(errors.IuguGeneralException, payment_test,
                                instance_payment.id)

    def test_set_payment_remove_by_attrs(self):
        """

        """
        instance_payment = self.customer.payment
        instance_payment.payment_data.description = "New payment method"
        instance_payment.payment_data.number = number='4111111111111111'
        instance_payment.payment_data.verification_value = 123
        instance_payment.payment_data.first_name = "Joao"
        instance_payment.payment_data.last_name = "Silva"
        instance_payment.payment_data.month = 12
        instance_payment.payment_data.year = 2015
        instance_payment = instance_payment.create(description="Meu cartao")
        instance_payment.remove()
        self.assertRaises(errors.IuguGeneralException, instance_payment.get, instance_payment.id)

    def test_getitems_payments(self):
        payment_one = self.customer.payment.create(description="New payment One",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="World", last_name="Cup",
                                     month=12, year=2014)
        payment_two = self.customer.payment.create(description="New payment Two",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="Is a ", last_name="Problem",
                                     month=12, year=2015)
        payment_three = self.customer.payment.create(description="New payment Three",
                                     number='4111111111111111',
                                     verification_value=123,
                                     first_name="To Brazil", last_name="Worry",
                                     month=12, year=2015)
        list_of_payments = self.customer.payment.getitems()
        self.assertTrue(isinstance(list_of_payments, list))
        self.assertTrue(isinstance(list_of_payments[0],
                                   customers.IuguPaymentMethod))


class TestInvoice(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.customer_email = email
        # create a customer for tests
        c = customers.IuguCustomer()
        self.consumer = c.create(email="client@customer.com")

        # create a invoice
        item = merchant.Item("Prod 1", 1, 1190)
        self.item = item
        self.invoice_obj = invoices.IuguInvoice(email=self.customer_email,
                                 item=item, due_date="30/11/2014")
        self.invoice = self.invoice_obj.create(draft=True)

    def tearDown(self):
        if self.invoice.id: # if id is None already was removed
            self.invoice.remove()
        self.consumer.remove()

    def test_invoice_raise_required_email(self):
        i = invoices.IuguInvoice()
        self.assertRaises(errors.IuguInvoiceException, i.create,
                          due_date="30/11/2020", items=self.item)

    def test_invoice_raise_required_due_date(self):
        i = invoices.IuguInvoice()
        self.assertRaises(errors.IuguInvoiceException, i.create,
                          email="h@gmail.com", items=self.item)

    def test_invoice_raise_required_items(self):
        i = invoices.IuguInvoice()
        self.assertRaises(errors.IuguInvoiceException, i.create,
                          due_date="30/11/2020", email="h@gmail.com")

    def test_invoice_create_basic(self):
        self.assertTrue(isinstance(self.invoice, invoices.IuguInvoice))

    def test_invoice_with_customer_id(self):
        res = self.invoice_obj.create(customer_id=self.consumer.id)
        self.assertEqual(res.customer_id, self.consumer.id)
        res.remove() # after because remove() "to zero" field

    def test_invoice_create_all_fields_as_draft(self):
        response = self.invoice_obj.create(draft=True, return_url='http://hipy.co/success',
                            expired_url='http://hipy.co/expired',
                            notification_url='http://hipy.co/webhooks',
                            tax_cents=200, discount_cents=500,
                            customer_id=self.consumer.id,
                            ignore_due_email=True)
        self.assertTrue(isinstance(response, invoices.IuguInvoice))
        existent_invoice = invoices.IuguInvoice.get(response.id)
        self.assertEqual(existent_invoice.expiration_url, response.expiration_url)
        response.remove()

    def test_invoice_create_all_fields_as_pending(self):
        response = self.invoice_obj.create(draft=False,
                            return_url='http://example.com/success',
                            expired_url='http://example.com/expired',
                            notification_url='http://example.com/webhooks',
                            tax_cents=200, discount_cents=500,
                            customer_id=self.consumer.id,
                            ignore_due_email=True)
        self.assertTrue(isinstance(response, invoices.IuguInvoice))
        response.remove()

    def test_invoice_created_check_id(self):
        self.assertIsNotNone(self.invoice.id)

    def test_invoice_get_one(self):
        # test start here
        res = invoices.IuguInvoice.get(self.invoice.id)
        self.assertEqual(res.items[0].description, "Prod 1")

    def test_invoice_create_as_draft(self):
        self.assertEqual(self.invoice.status, 'draft')

    def test_invoice_edit_email_with_set(self):
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id, email="now@now.com")
        self.assertEqual(invoice_edited.email, u"now@now.com")

    def test_invoice_edit_return_url_with_set(self):
        return_url = "http://hipy.co"
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              return_url=return_url)
        self.assertEqual(invoice_edited.return_url, return_url)

    def test_invoice_edit_with_set_only_id(self):
        id = self.invoice.id
        i = invoices.IuguInvoice()
        self.assertRaises(errors.IuguInvoiceException, i.set, id)

    @unittest.skip("It isn't support by API")
    def test_invoice_edit_expired_url_with_set(self):
        expired_url = "http://hipy.co"
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              expired_url=expired_url)
        self.assertEqual(invoice_edited.expiration_url, expired_url)

    def test_invoice_edit_notification_url_with_set(self):
        notification_url = "http://hipy.co"
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              notification_url=notification_url)
        self.assertEqual(invoice_edited.notification_url, notification_url)

    def test_invoice_edit_tax_cents_with_set(self):
        tax_cents= 200
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              tax_cents=tax_cents)
        self.assertEqual(invoice_edited.tax_cents, tax_cents)

    def test_invoice_edit_discount_cents_with_set(self):
        discount_cents = 500
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              discount_cents=discount_cents)
        self.assertEqual(invoice_edited.discount_cents, discount_cents)

    def test_invoice_edit_customer_id_with_set(self):
        customer_id = self.consumer.id
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              customer_id=customer_id)
        self.assertEqual(invoice_edited.customer_id, customer_id)

    @unittest.skip("Without return, but the logs could have it")
    def test_invoice_edit_ignore_due_email_with_set(self):
        ignore_due_email = True
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              ignore_due_email=ignore_due_email)
        self.assertEqual(invoice_edited.ignore_due_email, ignore_due_email)

    def test_invoice_edit_subscription_id_with_set(self):
        pass

    def test_invoice_edit_credits_with_set(self):
        pass

    def test_invoice_edit_due_date_with_set(self):
        due_date = "31/12/2014"
        id = self.invoice.id
        invoice_edited = self.invoice_obj.set(invoice_id=id,
                                              due_date=due_date)
        self.assertEqual(invoice_edited.due_date, u'2014-12-31')

    def test_invoice_edit_items_with_set(self):
        self.invoice.items[0].description = "Prod Fixed Text and Value"
        id = self.invoice.id
        items = self.invoice.items[0]
        invoice_edited = self.invoice_obj.set(invoice_id=id, items=items)
        self.assertEqual(invoice_edited.items[0].description, "Prod Fixed Text and Value")

    def test_invoice_changed_items_with_save(self):
        self.invoice.items[0].description = "Prod Saved by Instance"
        # inv_one is instance not saved. Now, we have invoice saved
        # and invoice_edited that is the response of webservice
        res = self.invoice.save()
        self.assertEqual(res.items[0].description, "Prod Saved by Instance")

    def test_invoice_destroy_item(self):
        # Removes one item, the unique, created in invoice
        self.invoice.items[0].remove()
        re_invoice = self.invoice.save()
        self.assertEqual(re_invoice.items, None)

    def test_invoice_remove(self):
        # wait webservice response time
        sleep(3)
        self.invoice.remove()
        self.assertEqual(self.invoice.id, None)

    def test_invoice_cancel(self):
        invoice = self.invoice_obj.create(draft=False)
        re_invoice = invoice.cancel()
        self.assertEqual(re_invoice.status, "canceled")
        invoice.remove()

    @unittest.skip("Support only invoice paid")
    def test_invoice_refund(self):
        re_invoice = self.invoice.refund()
        self.assertEqual(re_invoice.status, "canceled")

    def test_invoice_getitems(self):
        # wait webservice response time
        sleep(3)
        l = invoices.IuguInvoice.getitems()
        self.assertIsInstance(l, list)
        self.assertIsInstance(l[0], invoices.IuguInvoice)

    # TODO
    def test_invoice_getitems_limit(self):
        invoice_2 = self.invoice_obj.create()
        sleep(3)
        l = invoices.IuguInvoice.getitems(limit=2)
        invoice_2.remove()
        self.assertEqual(len(l), 2)

    def test_invoice_getitems_skip(self):
        invoice_1 = self.invoice_obj.create()
        invoice_2 = self.invoice_obj.create()
        invoice_3 = self.invoice_obj.create()
        sleep(3)
        l1 = invoices.IuguInvoice.getitems(limit=3)
        keep_checker = l1[2]
        l2 = invoices.IuguInvoice.getitems(skip=2)
        skipped = l2[0] # after skip 2 the first must be keep_checker
        invoice_1.remove()
        invoice_2.remove()
        invoice_3.remove()
        self.assertEqual(keep_checker.id, skipped.id)

    def test_invoice_getitems_created_at_from(self):
        pass # TODO

    def test_invoice_getitems_created_at_to(self):
        pass # TODO

    def test_invoice_getitems_updated_since(self):
        pass # TODO

    def test_invoice_getitems_query(self):
        res = self.invoice_obj.create(customer_id=self.consumer.id)
        sleep(3)
        queryset = invoices.IuguInvoice.getitems(query=res.id)
        self.assertEqual(queryset[0].customer_id, res.customer_id)
        res.remove()

    def test_invoice_getitems_customer_id(self):
        res = self.invoice_obj.create(customer_id=self.consumer.id)
        sleep(3)
        queryset = invoices.IuguInvoice.getitems(query=res.id)
        self.assertEqual(queryset[0].customer_id, res.customer_id)
        res.remove()

    @unittest.skip("API no support sort (in moment)")
    def test_invoice_getitems_sort(self):
        invoice_1 = self.invoice_obj.create()
        invoice_2 = self.invoice_obj.create()
        invoice_3 = self.invoice_obj.create()
        sleep(3)
        l1 = invoices.IuguInvoice.getitems(limit=3)
        keep_checker = l1[2]
        l2 = invoices.IuguInvoice.getitems(limit=3, sort="id")
        skipped = l2[0] # after skip 2 the first must be keep_checker
        invoice_1.remove()
        invoice_2.remove()
        invoice_3.remove()
        self.assertEqual(keep_checker.id, skipped.id)


class TestPlans(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        seed = randint(1, 199)
        variation = randint(4, 8)
        hash_md5.update(str(seed))
        identifier = hash_md5.hexdigest()[:variation]
        self.identifier = identifier # random because can't be repeated
        plan = plans.IuguPlan()
        self.plan = plan.create(name="My SetUp Plan", identifier=self.identifier,
                                     interval=1, interval_type="months",
                                     currency="BRL", value_cents=1500)

        # features
        self.features = plans.Feature()
        self.features.name = "Add feature %s" % self.identifier
        self.features.identifier = self.identifier
        self.features.value = 11

    def tearDown(self):
        self.plan.remove()

    def test_plan_create(self):
        plan = plans.IuguPlan()
        identifier = self.identifier + "salt"
        new_plan = plan.create(name="My first lib Plan", identifier=identifier,
                                     interval=1, interval_type="months",
                                     currency="BRL", value_cents=1000)
        self.assertIsInstance(new_plan, plans.IuguPlan)
        self.assertTrue(new_plan.id)
        new_plan.remove()

    def test_plan_create_without_required_fields(self):
        plan = plans.IuguPlan()
        self.assertRaises(errors.IuguPlansException, plan.create)

    def test_plan_create_features(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)
        # init object
        plan = plans.IuguPlan(name="Plan with features", identifier=identifier,
                                     interval=1, interval_type="months",
                                     currency="BRL", value_cents=1000)

        plan.features = [self.features,]
        new_plan_with_features = plan.create()
        self.assertIsInstance(new_plan_with_features.features[0], plans.Feature)
        self.assertEqual(new_plan_with_features.features[0].value, self.features.value)
        new_plan_with_features.remove()

    def test_plan_get(self):
        plan_id = self.plan.id
        plan = plans.IuguPlan.get(plan_id)
        self.assertEqual(self.identifier, plan.identifier)

    def test_plan_get_identifier(self):
        plan = plans.IuguPlan.get_by_identifier(self.identifier)
        self.assertEqual(self.identifier, plan.identifier)

    def test_plan_remove(self):
        plan = plans.IuguPlan()
        new_plan = plan.create(name="Remove me", identifier="to_remove",
                                     interval=1, interval_type="months",
                                     currency="BRL", value_cents=2000)
        removed_id = new_plan.id
        new_plan.remove()
        self.assertRaises(errors.IuguGeneralException,
                                        plans.IuguPlan.get, removed_id)

    def test_plan_edit_changes_name_by_set(self):
        plan_id = self.plan.id
        new_name = "New name %s" % self.identifier
        modified_plan = self.plan.set(plan_id, name=new_name)
        self.assertEqual(new_name, modified_plan.name)

    def test_plan_edit_changes_identifier_by_set(self):
        plan_id = self.plan.id
        new_identifier = "New identifier %s" % self.identifier
        modified_plan = self.plan.set(plan_id, identifier=new_identifier)
        self.assertEqual(new_identifier, modified_plan.identifier)

    def test_plan_edit_changes_interval_by_set(self):
        plan_id = self.plan.id
        new_interval = 3
        modified_plan = self.plan.set(plan_id, interval=new_interval)
        self.assertEqual(new_interval, modified_plan.interval)

    def test_plan_edit_changes_currency_by_set(self):
        plan_id = self.plan.id
        new_currency = "US"
        self.assertRaises(errors.IuguPlansException, self.plan.set,
                          plan_id, currency=new_currency)

    def test_plan_edit_changes_value_cents_by_set(self):
        plan_id = self.plan.id
        value_cents = 3000
        modified_plan = self.plan.set(plan_id, value_cents=value_cents)
        self.assertEqual(value_cents, modified_plan.prices[0].value_cents)

    def test_plan_edit_changes_features_name_by_set(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features Name"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        changed_features = plan_returned.features
        changed_features[0].name = "Changed Name of Features"

        # return plan changed
        plan_changed = plan.set(plan_returned.id, features=[changed_features[0]])

        self.assertEqual(plan_changed.features[0].name,
                         plan_returned.features[0].name)
        plan_returned.remove()

    def test_plan_edit_changes_features_identifier_by_set(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features Identifier"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        changed_features = plan_returned.features
        changed_features[0].identifier = "Crazy_Change"

        # return plan changed
        plan_changed = plan.set(plan_returned.id, features=[changed_features[0]])

        self.assertEqual(plan_changed.features[0].identifier,
                         plan_returned.features[0].identifier)
        plan_returned.remove()

    def test_plan_edit_changes_features_value_by_set(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features Identifier"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        changed_features = plan_returned.features
        changed_features[0].value = 10000

        # return plan changed
        plan_changed = plan.set(plan_returned.id, features=[changed_features[0]])

        self.assertEqual(plan_changed.features[0].value,
                         plan_returned.features[0].value)
        plan_returned.remove()

    def test_plan_edit_changes_name_by_save(self):
        self.plan.name = "New name %s" % self.identifier
        response = self.plan.save()
        self.assertEqual(response.name, self.plan.name)

    def test_plan_edit_changes_identifier_by_save(self):
        self.plan.identifier = "New_identifier_%s" % self.identifier
        response = self.plan.save()
        self.assertEqual(response.identifier, self.plan.identifier)

    def test_plan_edit_changes_interval_by_save(self):
        self.plan.interval = 4
        response = self.plan.save()
        self.assertEqual(response.interval, 4)

    def test_plan_edit_changes_currency_by_save(self):
        # API only support BRL
        self.plan.currency = "US"
        # response = self.plan.save()
        self.assertRaises(errors.IuguPlansException, self.plan.save)

    def test_plan_edit_changes_value_cents_by_save(self):
        self.plan.value_cents = 4000
        response = self.plan.save()
        self.assertEqual(response.prices[0].value_cents, 4000)

    def test_plan_edit_changes_features_name_by_save(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features by Save"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        to_change_features = plan_returned.features
        to_change_features[0].name = "Features New by Save"

        # return plan changed and to save instance
        plan_returned.features = [to_change_features[0]]
        plan_changed = plan_returned.save()

        self.assertEqual(plan_changed.features[0].name, "Features New by Save")
        plan_returned.remove()

    def test_plan_edit_changes_features_identifier_by_save(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features by Save"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        to_change_features = plan_returned.features
        to_change_features[0].identifier = "Crazy_Changed"

        # return plan changed and to save instance
        plan_returned.features = [to_change_features[0]]
        plan_changed = plan_returned.save()

        self.assertEqual(plan_changed.features[0].identifier, "Crazy_Changed")
        plan_returned.remove()

    def test_plan_edit_changes_features_value_by_save(self):
        salt = randint(1, 99)
        identifier = self.identifier + str(salt)

        # creating a plan with features
        plan = plans.IuguPlan()
        plan.features = [self.features,]
        plan.name = "Changes Features by Save"
        plan.identifier = identifier # workaround: setUp already creates
        plan.interval = 2
        plan.interval_type = "weeks"
        plan.currency = "BRL"
        plan.value_cents = 3000
        plan_returned = plan.create()

        # to change features name where features already has an id
        to_change_features = plan_returned.features
        to_change_features[0].value = 8000

        # return plan changed and to save instance
        plan_returned.features = [to_change_features[0]]
        plan_changed = plan_returned.save()

        self.assertEqual(plan_changed.features[0].value, 8000)
        plan_returned.remove()

    def test_plan_getitems_filter_limit(self):
        # creating a plan with features
        salt = str(randint(1, 199)) + self.identifier
        plan = plans.IuguPlan()
        plan_a = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=1000)
        salt = str(randint(1, 199)) + self.identifier
        plan_b = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=2000)
        salt = str(randint(1, 199)) + self.identifier
        plan_c = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=3000)

        all_plans = plans.IuguPlan.getitems(limit=3)
        self.assertEqual(len(all_plans), 3)
        plan_a.remove()
        plan_b.remove()
        plan_c.remove()

    def test_plan_getitems_filter_skip(self):
        # creating a plan with features
        salt = str(randint(1, 199)) + self.identifier
        plan = plans.IuguPlan()
        plan_a = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=1000)
        salt = str(randint(1, 199)) + self.identifier
        plan_b = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=2000)
        salt = str(randint(1, 199)) + self.identifier
        plan_c = plan.create(name="Get Items...",
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=3000)

        all_plans_limit = plans.IuguPlan.getitems(limit=3)
        all_plans_skip = plans.IuguPlan.getitems(skip=2, limit=3)
        self.assertEqual(all_plans_limit[2].id, all_plans_skip[0].id)
        plan_a.remove()
        plan_b.remove()
        plan_c.remove()

    def test_plan_getitems_filter_query(self):
        salt = str(randint(1, 199)) + self.identifier
        name_repeated = salt
        plan = plans.IuguPlan()
        plan_a = plan.create(name=name_repeated,
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=1000)
        salt = str(randint(1, 199)) + self.identifier
        plan_b = plan.create(name=name_repeated,
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=2000)
        salt = str(randint(1, 199)) + self.identifier
        plan_c = plan.create(name=name_repeated,
                                    identifier=salt, interval=2,
                                    interval_type="weeks", currency="BRL",
                                    value_cents=3000)
        sleep(3) # waiting API to keep data
        all_filter_query = plans.IuguPlan.getitems(query=name_repeated)
        self.assertEqual(all_filter_query[0].name, name_repeated)
        self.assertEqual(len(all_filter_query), 3)
        plan_a.remove()
        plan_b.remove()
        plan_c.remove()

    @unittest.skip("TODO support this test")
    def test_plan_getitems_filter_updated_since(self):
        pass
    @unittest.skip("Sort not work fine. Waiting support of API providers")
    def test_plan_getitems_filter_sort(self):
        pass


class TestSubscriptions(unittest.TestCase):

    def setUp(self):
        seed = randint(1, 299)
        md5_hash = md5()
        md5_hash.update(str(seed))
        plan_id_random = md5_hash.hexdigest()[:8]
        plan_name = "Subs Plan %s" % plan_id_random
        self.plan_new = plans.IuguPlan().create(plan_name, plan_id_random,
                                                1, "weeks", "BRL", 9900)
        name = "Ze %s" % plan_id_random
        email = "{name}@example.com".format(name=plan_id_random)
        self.client = customers.IuguCustomer().create(name=name, email=email)

    def tearDown(self):
        self.plan_new.remove()
        self.client.remove()

    def test_subscription_create(self):
        # Test to create a subscription only client_id and plan_identifier
        p_obj = subscriptions.IuguSubscriptions()
        subscription_new = p_obj.create(self.client.id, self.plan_new.identifier)
        self.assertIsInstance(subscription_new, subscriptions.IuguSubscriptions)
        self.assertEqual(subscription_new.plan_identifier, self.plan_new.identifier)
        subscription_new.remove()

    def test_subscription_remove(self):
        # Test to remove subscription
        p_obj = subscriptions.IuguSubscriptions()
        subscription_new = p_obj.create(self.client.id, self.plan_new.identifier)
        sid = subscription_new.id
        subscription_new.remove()
        self.assertRaises(errors.IuguGeneralException,
                                subscriptions.IuguSubscriptions.get, sid)

    def test_subscription_set_plan(self):
        # Test to change an existent subscription
        p_obj_t1 = subscriptions.IuguSubscriptions()
        subscription = p_obj_t1.create(self.client.id, self.plan_new.identifier)
        sid = subscription.id
        plan_identifier = self.plan_new.identifier + str("_Newest_ID")
        # changes to this new plan
        plan_newest = plans.IuguPlan().create("Plan Name: Newest", plan_identifier,
                                               1, "months", "BRL", 5000)
        # editing...
        subscription = subscriptions.IuguSubscriptions().set(sid,
                                        plan_identifier=plan_newest.identifier)
        self.assertEqual(subscription.plan_identifier, plan_identifier)
        subscription.remove()

    def test_subscription_set_customer_id(self):
        # Test if customer_id changed
        pass

    def test_subscription_set_expires_at(self):
        # Test if expires_at was changed
        pass

    def test_subscription_set_price_cents(self):
        # Test if customer_id changed
        pass

    def test_subscription_set_suspended(self):
        # Test if price_cents was changed
        pass

    def test_subscription_set_skip_charge(self):
        # Test if skip_charge was marked
        pass

    def test_subscription_set_subitems_description(self):
        # Test if subitem/item descriptions was changed
        pass

    def test_subscription_set_subitems_price_cents(self):
        # Test if subitem/item price_cents was  changed
        pass

    def test_subscription_set_subitems_quantity(self):
        # Test if subitem/item quantity was  changed
        pass

    def test_subscription_set_subitems_recurrent(self):
        # Test if subitem/item recurrent was  changed
        pass

    def test_subscription_set_subitems_destroy(self):
        # Test if subitem/item was erased
        pass

    def test_subscription_set_custom_variables(self):
        # Test if custom_variables changed
        pass

    def test_subscription_set_credits_cycle(self):
        # Test if credits_cycle changed
        pass

    def test_subscription_set_credits_min(self):
        # Test if credits_min changed
        pass
    pass
if __name__ == '__main__':
        unittest.main()
