from django.urls import path
from paymentIntrigation import views

urlpatterns = [
    path('address/', views.address,name="address"),
    path('payment/', views.payment,name="payment"),
    path('orderStatus/', views.orderStatus,name="orderStatus"),
]
