from django.contrib import admin
from django.urls import path
from landing_app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('allProducts/', views.allProducts, name="allProducts"),
    path('WinterProducts/', views.WinterProducts, name="WinterProducts"),
    path('SummerProducts/', views.SummerProducts, name="SummerProducts"),
    path('ShoesProducts/', views.ShoesProducts, name="ShoesProducts"),
    path('MoblieProducts/', views.MobileProducts, name="MobileProducts"),
    path('ElectronicsProducts/', views.ElectronicsProducts, name="ElectronicsProducts"),
    path('NewToCatchProducts/', views.NewToCatchProducts, name="NewToCatchProducts"),
    path('ToBrandsProducts/', views.ToBrandsProducts, name="ToBrandsProducts"),
    path('allProducts_iteams/', views.allProducts_iteams, name='allProducts_iteams'),
    path('products/<int:product_id>/', views.EachProductDetails, name='EachProductDetails'),
]