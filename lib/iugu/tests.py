#coding: utf-8

__author__ = 'horacioibrahim'

import unittest
from time import sleep, ctime, time
from random import randint
from hashlib import md5
from types import StringType

# python-iugu package modules
import merchant, customer


class TestMerchant(unittest.TestCase):

    def setUp(self):
        self.API_TOKEN_TEST = "3881a8eded982f25e12669b202b2b5df"
        self.EMAIL_CUSTOMER  = "horacioibrahim@gmail.com"

    def test_create_payment_token_is_test(self):
        client = merchant.IuguMerchant(account_id="25dfe5de-f86a-4507-89ed-922796bc05a8",
                                       api_mode_test=True)
        response = client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        self.assertTrue(response.is_test)

    def test_create_payment_token(self):
        client = merchant.IuguMerchant(account_id="25dfe5de-f86a-4507-89ed-922796bc05a8",
                                       api_mode_test=True)
        response = client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        self.assertEqual(response.status, 200)

    def test_create_charge_credit_card(self):
        item = merchant.Item("Produto My Test", 1, 10000)
        client = merchant.IuguMerchant(account_id="25dfe5de-f86a-4507-89ed-922796bc05a8",
                                       api_mode_test=True, api_token=self.API_TOKEN_TEST)
        token = client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                               '12', '2010', '123')
        charge = client.create_charge(self.EMAIL_CUSTOMER, item, token=token.id)
        self.assertEqual(charge.is_success(), True)

    def test_create_charge_blank_slip(self):
        item = merchant.Item("Produto Blank Slip", 1, 1000)
        client = merchant.IuguMerchant(account_id="25dfe5de-f86a-4507-89ed-922796bc05a8",
                                       api_mode_test=True, api_token=self.API_TOKEN_TEST)
        charge = client.create_charge(self.EMAIL_CUSTOMER, item)
        self.assertEqual(charge.is_success(), True)


class TestCustomer(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.API_TOKEN_TEST = "3881a8eded982f25e12669b202b2b5df"
        self.random_user_email = email


    def test_create_customer_basic_info(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        c = consumer.create()
        c.remove()
        self.assertEqual(consumer.email, c.email)

    def test_create_customer_extra_attrs(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        c = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        c.remove()
        self.assertEqual(consumer.email, c.email)

    def test_get_customer(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        consumer_new = consumer.create()
        c = consumer.get(customer_id=consumer_new.id)
        consumer_new.remove()
        self.assertEqual(consumer.email, c.email)

    def test_set_customer(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        c = consumer.set(consumer_new.id, name="Lago Mario")
        consumer_new.remove()
        self.assertEqual(c.name, "Lago Mario")

    def test_customer_save(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
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
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])
        r = consumer.delete(consumer_new.id)
        self.assertRaises(TypeError, consumer.get, consumer_new.id)

    def test_customer_delete_instance(self):
        consumer = customer.IuguCustomer(api_mode_test=True,
                                         api_token=self.API_TOKEN_TEST,
                                         email=self.random_user_email)
        consumer_new = consumer.create(name="Mario Lago", notes="It's the man",
                                     custom_variables=["local", "cup"])

        r = consumer_new.remove()
        self.assertRaises(TypeError, consumer.get, consumer_new.id)


class TestCustomerLists(unittest.TestCase):

    def setUp(self):
        hash_md5 = md5()
        number = randint(1, 50)
        hash_md5.update(str(number))
        email = "{email}@test.com".format(email=hash_md5.hexdigest())
        self.API_TOKEN_TEST = "3881a8eded982f25e12669b202b2b5df"
        self.random_user_email = email

        self.c = customer.IuguCustomer(api_mode_test=True,
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
        customers = self.c.getitems()
        self.assertEqual(type(customers), list)

    def test_getitems_limit(self):
        # get items with auto DESC order
        customers = self.c.getitems(limit=2)
        self.assertEqual(len(customers), 2)

    def test_getitems_start(self):
        # get items with auto DESC order
        sleep(2)
        customers = self.c.getitems(limit=3) # get latest three customers
        reference_customer = customers[2].name
        customers = self.c.getitems(skip=2)
        self.assertEqual(customers[0].name, reference_customer)

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
        customer = self.c.create(email=email)
        sleep(2)
        items = self.c.getitems(query=term)
        customer.remove()
        self.assertIn(term, items[0].email)

    # Uncomment/comment the next one line to disable/enable the test
    @unittest.skip("Database of webservice is not empty")
    def test_getitems_sort(self):
        sleep(1) # Again. It's need
        # Useful to test database with empty data (previous data, old tests)
        customers = self.c.getitems(sort="name")

        # monkey skip
        if len(customers) < 4:
            self.assertEqual(customers[0].name, self.p1)
        else:
            raise TypeError("API Database is not empty. This test isn't useful. " \
                "Use unittest.skip() before this method.")

    def test_getitems_created_at_from(self):
        sleep(1)
        customers = self.c.getitems(created_at_from=self.three.created_at)
        self.assertEqual(customers[0].id, self.three.id)

    # Uncomment the next one line to disable the test
    # @unittest.skip("Real-time interval not reached")
    def test_getitems_created_at_to(self):
        sleep(1)
        customers = self.c.getitems(created_at_to=self.one.created_at)
        self.assertEqual(customers[0].id, self.three.id)

    def test_getitems_updated_since(self):
        # get items with auto DESC order
        sleep(1)
        customers = self.c.getitems(updated_since=self.three.created_at)
        self.assertEqual(customers[0].id, self.three.id)

if __name__ == '__main__':
        unittest.main()