from django.contrib import messages


import json
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView

# Create your views here.
from . import settings
from paystack.api import signals
from paystack import utils
from paystack.api.signals import payment_verified
from paystack.utils import load_lib

from shop.models import Order
from django.contrib.auth.models import User


def verify_payment(request, order):
    amount = request.GET.get("amount")
    txrf = request.GET.get("trxref")
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_payment(txrf, amount=int(amount))
    if response[0]:
        payment_verified.send(
            sender=PaystackAPI, ref=txrf, amount=int(amount) / 100, order=order
        )
        #Logic responsible for updating the ordered to True
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        order.ordered = True
        order.save()
        
        messages.info(request, "Payment Successful. Continue Shopping")
        return redirect(reverse("paystack:successful_verification", args=[order]))
    messages.info(request, "Verification of payment failed. Please Check and try again.")    
    return redirect(reverse("paystack:failed_verification", args=[order]))


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_FAILED_URL == "paystack:failed_page":
            return reverse(settings.PAYSTACK_FAILED_URL)
        return settings.PAYSTACK_FAILED_URL


def success_redirect_view(request, order_id):
    url = settings.PAYSTACK_SUCCESS_URL
    if url == "paystack:success_page":
        url = reverse(url)
    return redirect(url, permanent=True)


def failure_redirect_view(request, order_id):
    url = settings.PAYSTACK_FAILED_URL
    if url == "paystack:failed_page":
        url = reverse(url)
    return redirect(url, permanent=True)


class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_SUCCESS_URL == "paystack:success_page":
            return reverse(settings.PAYSTACK_SUCCESS_URL)
        return settings.PAYSTACK_SUCCESS_URL


def webhook_view(request):
    # ensure that all parameters are in the bytes representation
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    signature = request.META["HTTP_X_PAYSTACK_SIGNATURE"]
    paystack_instance.webhook_api.verify(signature, request.body, full_auth=True)
    # digest = utils.generate_digest(request.body)
    # if digest == signature:
    #     payload = json.loads(request.body)
    #     signals.event_signal.send(
    #         sender=request, event=payload['event'], data=payload['data'])
    return JsonResponse({"status": "Success"})
