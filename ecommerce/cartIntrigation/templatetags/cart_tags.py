from django import template
from landing_app.models import Product
from landing_app.views import *
register = template.Library()

@register.simple_tag
def get_product_details(items_id):
    product_details=Product.objects.get(id=int(items_id))
    return product_details

@register.simple_tag
def get_quantity_of_each_product(request,items_id): 
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(items_id)
    return quantity

@register.simple_tag
def get_product_price(request,items_id):
    product_details=Product.objects.get(id=int(items_id))
    quantity=get_quantity_of_each_product(request,items_id)
    price=product_details.price
    return quantity * price

@register.simple_tag
def get_total_product_price(request,items_ids):
    total_price = 0
    cart=request.session.get('cart')
    for item_id in items_ids:
        try:
            quantity=cart.get(item_id)
            for i in range(quantity):
                product = Product.objects.get(id=item_id)
                total_price += product.price  # Adjust based on your model's price attribute
        except Product.DoesNotExist:
            continue  # Handle the case where the product does not exist
    return total_price
    
    

