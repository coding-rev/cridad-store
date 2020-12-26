from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegisterForm

from django.contrib import messages

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
       # email = RegisterForm.EmailField()
        if form.is_valid():
            form.save()
            #send_mail(
            #    'Jays Detergents',
            #    'Congratulations! you have successfully created an account.',
            #    settings.EMAIL_HOST_USER,
            #    [email],
            #    fail_silently=False)
           
            return redirect('/login')
    else:
        form = RegisterForm()

    return render(response, "register.html", {"form":form})
