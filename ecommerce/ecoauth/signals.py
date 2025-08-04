from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save,sender=User)
def after_user_activated(sender,instance,**kwargs):
    if instance.is_active:
        print(f"MyModel instance updated: {instance.is_active}")