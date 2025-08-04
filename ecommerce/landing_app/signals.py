from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver,Signal
from landing_app.models import Product
from django.core.cache import cache

#  define signal

session_update_singal=Signal()


@receiver(session_update_singal)
def handle_session_update(sender,request,**kwargs):
    cache.delete_pattern('*product_category*')
    print("cache.deleted")
@receiver([post_delete,post_save],sender=Product)
def invalidate_product_cache(sender,instance,**kwargs):
    print("Clearing product cache")
    # request.session['cart'] = cart


