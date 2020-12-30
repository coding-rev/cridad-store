from django.conf import settings

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Wish, WishItem, Item, OrderItem, Order, Billingshop ,CommentForm, Comment, Category

from .forms import CheckoutForm, UserUpdateForm

#TODO: Allow users to change their password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password

@login_required
def change_password(request):
    currentpassword = request.user.password #user's current password
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/user-dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', {'form':form})


@login_required
def Dashboard(request):
    try:
        items = Item.objects.all()
        order = Order.objects.get(user=request.user, ordered=False)
        wish = Wish.objects.get(user=request.user)
        history = Billingshop.objects.filter(user=request.user)
        #Handling user profile update
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            
            if user_form.is_valid():
                user_form.save()
                messages.success(request, f'Your account has been updated!')
                return HttpResponseRedirect(url)

        else:
            user_form = UserUpdateForm(instance=request.user)
           
        #User profile update ends here
            context = {
                "items":items,
                "object":order,
                'wish':wish,
                'history':history,
                'user_form': user_form,
            }
        return render(request, "dashboard.html", context)

    except:
        user_form = UserUpdateForm(instance=request.user)
        items = Item.objects.all()
        history = Billingshop.objects.filter(user=request.user)
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            
            if user_form.is_valid():
                user_form.save()
                messages.success(request, f'Your account has been updated!')
                return HttpResponseRedirect(url)
        context = {
            "items":items,
            'history':history,
            'user_form': user_form,
        }
        return render(request, "dashboard.html", context)

def Home(request):
    try:
        items = Item.objects.all()
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            "items":items,
            "object":order,
        }
        return render(request, "index.html", context)

    except:
        items = Item.objects.all()
        context = {
            "items":items,
        }
        return render(request, "index.html", context)
	
def Shop(request):
    try:
        items = Item.objects.all()
        category = Category.objects.all()
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            "items":items,
            "category":category,
            "object":order,
        }
        return render(request, "shop.html", context)
    except:
        items = Item.objects.all()
        context = {
            "items":items,
            "category":category,
        }
        return render(request, "shop.html", context)


def product_detail(request,pk):
    try:
        item = Item.objects.get(pk=pk)
        others = Item.objects.filter(category=item.category)
        comments= Comment.objects.filter(item_id=pk)
        order = Order.objects.get(user=request.user, ordered=False)

        context ={
            'item':item,
            'comments':comments,
            'others':others,
            'object':order,
        }
        return render(request, 'product-details.html', context)
    except:
        item = Item.objects.get(pk=pk)
        others = Item.objects.filter(category=item.category)
        comments = Comment.objects.filter(item_id=pk)
        context={
            'item':item,
            'comments':comments,
            'others':others,
        }
        return render(request, 'product-details.html', context)

@login_required
def product_detail_for_login(request,pk):
    try:
        item = Item.objects.get(pk=pk)
        others = Item.objects.filter(category=item.category)
        comments= Comment.objects.filter(item_id=pk)
        order = Order.objects.get(user=request.user, ordered=False)

        context ={
            'item':item,
            'comments':comments,
            'others':others,
            'object':order,
        }
        return render(request, 'product-details.html', context)
    except:
        item = Item.objects.get(pk=pk)
        others = Item.objects.filter(category=item.category)
        comments = Comment.objects.filter(item_id=pk)
        context={
            'item':item,
            'comments':comments,
            'others':others,
        }
        return render(request, 'product-details.html', context)


def addcomment(request, pk):
    url = request.META.get('HTTP_REFERER')
    #return HttpResponse(url)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.item_id = pk 
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.info(request, "Your Review has been sent. Thanks for your feedback.")
            return HttpResponseRedirect(url)
        else:
            messages.info(request, "Failed. Your form was not valid")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)



# search function ends here
class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form':form,
                'object': order
            }
            return render(self.request, "checkout.html",context)
        except ObjectDoesNotExist:
            return render(self.request, 'checkout.html')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                phone = form.cleaned_data.get('phone')
                country = form.cleaned_data.get('country')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                town = form.cleaned_data.get('town')
                region = form.cleaned_data.get('region')
                postal = form.cleaned_data.get('postal')
                # TODO: and functionality for these fields
                #save_billing_address = form.cleaned_data.get('save_billing_address')
                #save_info = form.cleaned_data.get('save_info')
                billing_address = Billingshop(
                    user=self.request.user,
                    phone=phone,
                    country=country,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    region=region,
                    town=town,
                    postal=postal,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect("shop:payment")                    
            
            return redirect("shop:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("shop:order-summary")


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'payment.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'payment.html')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'cart.html')

class OrderSummaryRawView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'cart.html')

class WishView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            wish = Wish.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': wish
            }
            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            return render(self.request, "wishlist.html")

class WishRawView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            wish = Wish.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': wish
            }
            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            return render(self.request, "wishlist.html")




# Creating a function for Add to Cart
@login_required
def add_to_cart (request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user= request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            messages.info(request, "Item already in cart")
        else:
            messages.info(request, "This item was added to your cart successfully")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart successfully")
    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)

@login_required
def add_to_wish(request, pk):
    item = get_object_or_404(Item, pk=pk)
    wish_item, created = WishItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    wish_qs = Wish.objects.filter(user=request.user, ordered=False)
    if wish_qs.exists():
        wish = wish_qs[0]
        # check if the order item is in the order
        if wish.items.filter(item__pk=item.pk).exists():
            wish_item.save()
            messages.info(request, "This item is already in your wish list")
        else:
            messages.info(request, "This item was added to your wish list")
            wish.items.add(wish_item)

    else:
        ordered_date = timezone.now()
        wish = Wish.objects.create(
            user=request.user, ordered_date=ordered_date)
        wish.items.add(wish_item)
        messages.info(request, "This item was added to your wish list")
    return redirect("shop:wishlist", pk=pk)

# add to cart in category
@login_required
def add_to_cart_category(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user= request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item quantity was updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)


# creating remove from cart
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart successfully")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
        else:
            # add a message saying the user doesn't have an order
            messages.info(request, "This item was not in your cart")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
    else:
        #add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)
    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)

@login_required
def remove_from_wish(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Wish.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = WishItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your wishlist")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
        else:
            # add a message saying the user doesn't have an order
            messages.info(request, "This item was not in your wishlist")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
    else:
        #add a message saying the user doesn't have an order
        messages.info(request, "You do not have any wish item")
        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)
    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)

# the plus and minus signs in cart
@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Item quantity updated")
            else:
                order.items.remove(order_item)
                messages.info(request, "Item removed from cart")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
        else:
            # add a message saying the user doesn't have an order
            messages.info(request, "This item was not in your cart")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
    else:
        #add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)



@login_required
def add_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
        else:
            # add a message saying the user doesn't have an order
            messages.info(request, "This item was not in your cart" )
            url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(url)
    else:
        #add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)


# ORDER EXCEPTIONAL PAGES

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def blog_single(request):
    return render(request, 'blog-single.html')

def accomodation(request):
    return render(request, 'accomodation.html')

def about(request):
    return render(request, 'about.html')


