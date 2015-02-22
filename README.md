Iugu python API
============================================

Iugu python compatible client for Iugu API v1

Overview
--------
This package contains the lib code used to call the Iugu API from Python.

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

Quick Install
-----
### Using pip ###
```
pip install git+https://github.com/horacioibrahim/iugu-python.git
```
or
### Using setup.py ###
```
# Downloading package master or release:
# https://github.com/horacioibrahim/iugu-python/archive/master.zip
# or https://github.com/horacioibrahim/iugu-python/releases
unzip iugu-python-master.zip
cd iugu-python-master
python setup.py install
```

Usage (Quick Start)
-----
### Export environment variable IUGU_API_TOKEN ###
```
# For linux users:
export IUGU_API_TOKEN=XXX
```
### Merchant operations ###
```
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
Check invoice ID created. All payment pass by Invoice.
```
charge.invoice_id
```
Or create a blank_slip ("Boleto Bancário")
```
charge = client.create_charge(EMAIL_CUSTOMER, item)
 => https://api.iugu.com/v1/charge
```
### Customer operations ###
```python
from iugu.customers import IuguCustomer
client = IuguCustomer()
customer = client.create(email='your_customer@example.com')
 => https://api.iugu.com/v1/customers
```
Now you can to retrieve customer
```
client.get(customer_id)
```
You can edit existent customer
```
client.set(CUSTOMER_ID, name="Sub Zero Wins")
```
Or you can to use save()
```
customer.name = "Sub Zero Wins"
customer.save()
```
To remove or delete customer
```
client.delete(CONSUMER_ID) # by id
 or
customer.remove() # by current instance
```
### Operations with lists of customer ###
Get all customer
```python
from iugu.customers import IuguCustomer
client = IuguCustomer()
# your flavor of options
# client.getitems([limit, skip, query, sort, created_at_from, created_at_to,
#                updated_since])

Use one option per time. Samples:
client.getitems(limit=30) # Get most recent (latest) 30 customers
client.getitems(skip=14) # Skip X customers. Useful for pagination
client.getitems(updated_since="2014-06-05T15:02:40-03:00")

In tests SORT is not support by API:
client.getitems(sort="-name") # Sort by field >>name<< (descending)
client.getitems(sort="name") # Sort by field >>name<< (ascending)

 => http://iugu.com/referencias/api#listar-os-clientes
```
### Operations with Invoices ###
Create an invoice
```
from iugu.invoices import IuguInvoice
from iugu.merchant import Item

item = Item("Curso: High Self Learning", 1, 6900) # qtd:1; price: 69,00
invoice_obj = IuguInvoice()
new_invoice = invoice_obj.create(due_date='24/06/2014',
                                    email='customer@example.com', items=item)
```
Get invoice by id
```
# not is need previous instance/obj (classmethod)
invoice_existent = IuguInvoice.get('A4AF853BC5714380A8708B2A4EDA27B3')
```
Get all invoices
```
# not is need previous instance/obj
invoices = IuguInvoice.getitems() # outcomes list of invoices (max 100 by API)
```
Get all with filter
```
invoices = IuguInvoice.getitems(limit=10)
invoices = IuguInvoice.getitems(skp=5)
invoices = IuguInvoice.getitems(sort="-email") # DESC
invoices = IuguInvoice.getitems(sort="email") # ASC
...
```
Edit/change invoice. Only invoices with status "draft" can be changed all fields
otherwise (if status pending, cancel or paid) only the logs field can to change
```
invoice_existent = IuguInvoice.get('A4AF853BC5714380A8708B2A4EDA27B3')
invoice_existent.email = "other@other.com"
invoice_existent.save()
```
Remove
```
invoice_existent.remove()
```
Cancel
```
IuguInvoice.to_cancel('A4AF853BC5714380A8708B2A4EDA27B3')
```
Refund
```
invoice_existent = IuguInvoice.get('A4AF853BC5714380A8708B2A4EDA27B3')
invoice_existent.refund()
```
### Operations with Subscriptions ###
Create a subscription
```
from subscriptions import IuguSubscription
client = IuguSubscription()
# from plans import IuguPan
# plan_x = IuguPlan().create("Plano Collor", "plano_collor")
# from customers import IuguCustomer
# mario = IuguCustomer().create(email='supermario@gmail.com')
# subscription = client.create(customer_id=mario.id,
#                 plan_identifier=plan_x.identifier)
subscription = client.create(customer_id="XXX", plan_identifier="XXX")
```
Get one
```
subscription = IuguSubscription.get('ID')
```
Edit/Change
```
subscription = IuguSubscription.get('ID')
subscription.expires_at = "14/07/2014"
subscription.save()
```
Remove
```
subscription.remove()
```

### References ###
- API Document: http://iugu.com/referencias/api


Known Issues
------------
### Date Types ###
It's need to use date formatted as string "2014-06-05T15:02:40-03:00",
but in new release date will python date.
