from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from landing_app.models import Product
from django.core.cache import cache



@receiver([post_delete,post_save],sender=Product)
def invalidate_product_cache(sender,instance,**kwargs):
    cache.delete_pattern("*product*")


