import stripe
from decouple import config



DJANGO_DEBUG = config('DJANGO_DEBUG',default=False,cast=bool)
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY',default="",cast=str)


if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise  ValueError("Invalid stripe key for production")



stripe.api_key = STRIPE_SECRET_KEY

def create_customer(name="",email="",metadata={},raw=False):
    response = stripe.Customer.create (
        name=name,
        email=email,
        metadata=metadata
    )
    if raw:
        return response

    stripe_id = response.id
    return stripe_id


def create_product(name="",metadata={},raw=False):
    response = stripe.Product.create(
        name = name,
        metadata=metadata
    )
    if raw:
        return response
    stripe_id = response.id
    return stripe_id



def create_product_price(product,price,currency_type="usd",interval="month",metadata={},raw=False):
    response = stripe.Price.create(
    currency=currency_type,
    unit_amount=price,
    product= product,
    recurring = {"interval":interval},
    metadata=metadata
    )

    if raw:
        return response
    stripe_id = response.id
    return stripe_id


