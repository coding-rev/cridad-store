from django import template
from shop.models import Order, Wish

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs= Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def wish_item_count(user):
    if user.is_authenticated:
        qs = Wish.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0