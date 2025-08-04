from django.urls import path
from cartIntrigation import views
  
urlpatterns = [
    path('cart_summery/', views.cart_summery, name="cart_summery"),
    path('quntity_add//<int:product_id>/', views.quntity_add, name="quntity_add"),
    path('cart_delete/<int:product_id>/', views.cart_delete, name='cart_delete'),
    path('remove//<int:product_id>/', views.quntity_remove, name="quntity_remove",),
    path('Checkout/', views.Checkout, name='Checkout')

   ]
