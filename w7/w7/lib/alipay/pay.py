from . import settings
from alipay import AliPay


alipay = AliPay(
    appid=settings.APPID,
    app_notify_url=None,
    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
    sign_type=settings.SIGN_TYPE,
    debug=settings.DEBUG
)


gateway = settings.GATEWAY