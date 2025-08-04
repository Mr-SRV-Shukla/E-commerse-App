from django.contrib import admin

# Register your models here.

from .models import Orders,OrdersUpdate
admin.site.register(Orders)
admin.site.register(OrdersUpdate)

