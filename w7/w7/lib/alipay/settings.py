import os


APPID = '9021000134680017'

APP_PRIVATE_KEY_STRING = open(os.path.join(os.path.dirname(__file__), 'pem', 'private_key.pem')).read()
ALIPAY_PUBLIC_KEY_STRING = open(os.path.join(os.path.dirname(__file__), 'pem', 'public_key.pem')).read()

SIGN_TYPE = 'RSA2'

DEBUG = True

GATEWAY = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' if DEBUG else 'https://openapi-sandbox.dl.alipay.com/gateway.do?'