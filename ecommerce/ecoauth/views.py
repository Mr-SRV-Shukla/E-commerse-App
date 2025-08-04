# Core Django imports
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View

# Authentication and User Management
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Site and Encoding Utilities
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Email Functionality
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string

# Custom Token Generators
from .utils import TokenGenerator, generate_token

# reset-password generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading 

# Email Thread class to handle email sending in a separate thread
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

                
# signUp page 
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.warning(request, "Email is already taken")
            return redirect("signup")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)

        # Construct the activation URL
        activation_url = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"

        mail_subject = "Please activate your account"
        message = render_to_string("auth/activate.html", {
            "user": user,
            "domain": current_site.domain,
            "uid": uid,
            "token": token,
            "activation_url": activation_url,
        })

        email_message = EmailMessage(
            mail_subject, message, settings.EMAIL_HOST_USER, [email]
        )
        EmailThread(email_message).start()

        messages.info(request, "Activate your account by clicking the link in your email")
        return redirect("hendleLogin")

    return render(request, "auth/signup.html")
# hendleLogin 
def hendleLogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")
        else:
            messages.warning(request, "Invalid username or password")
            return redirect("hendleLogin")

    return render(request, "auth/login.html")


# heandle Logout
def hendelLogout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("hendleLogin")

#  activate Account concept
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            print(user.is_active)
            user.is_active=True
            print(user.is_active)
            user.save()
            print(user.is_active)
            messages.info(request,"Account activated Successfully")
            return redirect("hendleLogin")
        return render(request,"auth/activatefail.html")


# RequestResetEmailView 
class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'auth/request-reset-email.html')

    def post(self, request):  # Lowercase "post"
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            current_site = get_current_site(request)
            email_subject = '[Reset Your Password]'
            message = render_to_string(
                'auth/reset-user-password.html',
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": PasswordResetTokenGenerator().make_token(user),
                }
            )
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email]
            )
            email_message.send()

            messages.info(request, "We have sent you an email with instructions on how to reset your password.")
            return redirect('reset-email')  # Redirect instead of rendering the same page

        messages.error(request, "No account found with that email.")
        return redirect('reset-email')
           
class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            "uidb64": uidb64,
            "token": token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            # Check if the token is valid
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password reset link is invalid or expired.")
                return redirect("reset-email")
        except (DjangoUnicodeDecodeError, User.DoesNotExist) as identifier:
            messages.warning(request, "Something went wrong. Please try again.")
            return redirect("reset-email")

        return render(request, "auth/set-new-password.html", context)

    def post(self, request, uidb64, token):
        context = {
            "uidb64": uidb64,
            "token": token,
        }

        password = request.POST.get("pass1")
        confirm_password = request.POST.get("pass2")

        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Passwords do not match.")
            return render(request, "auth/set-new-password.html", context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            # Update the user's password
            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successfully. Please login with your new password.")
            return redirect("hendleLogin")
        except (DjangoUnicodeDecodeError, User.DoesNotExist) as identifier:
            messages.warning(request, "Something went wrong. Please try again.")
            return render(request, "auth/set-new-password.html", context)