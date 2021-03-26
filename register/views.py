from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegisterForm

from django.contrib import messages

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            form.save()
            subject = 'Welcome to Cridad Store'
            message = """
We are glad you've joined the cridad community. Thank you for choosing us. 
Cridad Store was built with you in mind. Fully complete your profile, 
explore the app and start making the best and affordable purchases in your comfort zone.

To your success,
Cridad Team
"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list, fail_silently=True)
            return redirect('/login')
    else:
        form = RegisterForm()

    return render(response, "register.html", {"form":form})
