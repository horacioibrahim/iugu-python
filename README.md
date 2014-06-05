Iugu python SDK
============================================

Iugu python compatible client for Iugu API v1

Overview
--------
This package contains wrapper code used to call the Iugu from Python.

The package also contains a sample script. The code demonstrates the basic use
of the package for single client.

Prerequisites
-------------
In order to use the code in this package, you need to obtain an account
(API key) from http://iugu.com/referencias/api. You'll also find full API
documentation on that page.

In order to run the sample code, you need a user account on the test mode
service where you will do your development. Sign up for an account at
https://iugu.com/signup and change mode in https://iugu.com/a/administration
("Modo de Teste")

In order to run the client sample code, you need a account user token. This is
automatically created. See https://iugu.com/settings/profile

Usage (Quick Start)
-----
### Merchant operations ###
```python
from iugu.merchant import IuguMerchant, Item
client = IuguMerchant(account_id="YOUR ACCOUN ID",
                              api_mode_test=True)
token = client.create_payment_token('4111111111111111', 'JA', 'Silva',
                                                    '12', '2010', '123')
 => https://api.iugu.com/v1/payment_token
```
How create an item for charge
```
item = Item("Produto My Test", 1, 10000)
```
Now you can to create charge
```python
charge = client.create_charge(EMAIL_CUSTOMER, item, token=token.id)
```
Or create a blank_slip (In Brazil "Boleto Bancário")
```
client.create_charge(EMAIL_CUSTOMER, item)
 => https://api.iugu.com/v1/charge
```
### Customer operations ###
```python
from iugu.customer import IuguCustomer
client = IuguCustomer(api_mode_test=True,
                      api_token='YOUR API KEY',
                      email='YOUR EMAIL')
customer = consumer.create(email='your_customer@example.com')
 => https://api.iugu.com/v1/customers
```
Now you can to retrieve customer with set()
```
client.get(customer_id='ID')
```
You can edit existent customer
```
client.set(CUSTOMER_ID, name="Sub Zero Wins")
```
Or you can use save()
```
customer.name = "Sub Zero Wins"
customer.save()
```
To remove or delete customer
```
client..delete(CONSUMER_ID)
 or
customer.remove()
```
### Operations with lists of customer ###
Get all customer
```python
from iugu.customer import IuguCustomer
client = IuguCustomer(api_mode_test=True,
                      api_token='YOUR API KEY',
                      email='YOUR EMAIL')
client.getitems([limit, skip, query, sort, created_at_from, created_at_to,
                updated_since])

Use one option per time:
client.getitems(limit=30)
client.getitems(skip=14) # useful for pagination
client.getitems(sort="-name") # sort by field name (DESC)
client.getitems(sort="name") # sort by field name (ASC)
client.getitems(updated_since="2014-06-05T15:02:40-03:00")
```

### References ###
- API Document: http://iugu.com/referencias/api


Known Issues
------------
### Date Types ###
It's need to use date formatted as string "2014-06-05T15:02:40-03:00",
but in new release date will python date.

