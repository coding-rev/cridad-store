from django.conf import settings
from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from django.contrib.auth.forms import UserCreationForm

# Create your models here.
LABEL_CHOICES =[
    ('New', 'New'),
    ('Featured', 'Featured'),
    ('Promo', 'Promo'),
]

SIZE_CHOICES = [
	('XS', 'XS'),
	('S','S'),
	('M', 'M'),
	('L', 'L'),
	('XL', 'XL'),
	('XXL', 'XXL'),
]

class Advert(models.Model):
    picture = models.ImageField(upload_to='gallery/items')
    mobile_pic = models.ImageField(default='mobile-slide.jpg' ,upload_to='gallery/items')
    subject = models.CharField(max_length=12)
    content = models.CharField(max_length=20)
    other = models.CharField(max_length=8)

    class Meta:
        verbose_name_plural = 'ADVERTISEMENT SECTION'

    def __str__(self):
        return self.subject

class SubAdvert(models.Model):
    picture = models.ImageField(upload_to='gallery/items')
    subject = models.CharField(max_length=12)
    content = models.CharField(max_length=20)
    other = models.CharField(max_length=8)

    class Meta:
        verbose_name_plural = 'SUB ADVERTS'

    def __str__(self):
        return self.subject

class Category(models.Model):
	category = models.CharField(max_length=20, unique=True)
	def __str__(self):
		return self.category


class Item(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='gallery/items')
    photo_back = models.ImageField(upload_to='gallery/items')
    photo_three = models.ImageField(default='mobile-slide.jpg', upload_to='gallery/items')
    photo_four = models.ImageField(default='mobile-slide.jpg', upload_to='gallery/items')
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=100,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    delivery_and_returns = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=20)
    size = models.CharField(choices=SIZE_CHOICES, max_length=10, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=30, blank=True, null=True)
    deal_of_the_day = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'ADD | VIEW PRODUCTS'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'pk': self.pk
        })

    
    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'pk': self.pk
        })

    def get_add_to_wish_url(self):
        return reverse("shop:add-to-wish", kwargs={
            'pk': self.pk
        })

    def get_add_to_cart_category_url(self):
        return reverse("shop:add_to_cart_category", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'pk': self.pk
        })

class Comment(models.Model):
    STATUS = {
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    }

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    class Meta:
        verbose_name_plural = 'REVIEWS'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class WishItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Wish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(WishItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name_plural = 'INITIAL ORDER'

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount

    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount:
            return self.get_total_discount_item_price()
        return self.get_total_item_price() 


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    billing_shop = models.ForeignKey(
        'Billingshop', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'USERS-ORDERED'

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Billingshop(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address= models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    postal = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'BILLING ADDRESS'

    def __str__(self):
        return self.user.username
