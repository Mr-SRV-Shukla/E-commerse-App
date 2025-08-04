from django.contrib import admin
from django.urls import path
from .views import RequestResetEmailView
from ecoauth import views
  
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('hendleLogin/',views.hendleLogin,name="hendleLogin"),
    path('hendleLogout/',views.hendelLogout,name="hendelLogout"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('reset-email/', RequestResetEmailView.as_view(), name='reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(), name="set-new-password"),
    
]
