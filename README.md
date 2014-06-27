Iugu python API
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
from iugu.customer import IuguCustomer
client = IuguCustomer()
# your flavor of options
# client.getitems([limit, skip, query, sort, created_at_from, created_at_to,
#                updated_since])

Use one option per time. Samples:
client.getitems(limit=30) # Get most recent (latest) 30 customers
client.getitems(skip=14) # Skip X customers. Useful for pagination
client.getitems(sort="-name") # Sort by field >>name<< (descending)
client.getitems(sort="name") # Sort by field >>name<< (ascending)
client.getitems(updated_since="2014-06-05T15:02:40-03:00")

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
# not is need previous instance/obj
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
Edit/change invoice
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
### URN in single local ###
TODO: to create make_urn([])

