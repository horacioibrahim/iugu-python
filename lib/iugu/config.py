__author__ = 'horacioibrahim'


METHOD_PAYMENT_CREDIT_CARD = "credit_card"

DEBUG = False # Print logs/messages in console.


# No share data
API_HOSTNAME = "api.iugu.com"
ACCOUNT_EMAIL  = "YOUR_EMAIL@gmail.com"
ACCOUNT_ID = "YOUR-ACCOUNT-ID-OF-API"
API_MODE_TEST = True # default False
API_TOKEN_TEST = "YOUR_HASH_TOKEN_TEST"
if API_MODE_TEST:
    API_TOKEN = API_TOKEN_TEST # Change it in production
else:
    API_TOKEN = "YOUR_TOKEN_PRODUCTION"
