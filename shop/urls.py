from django.urls import path
from .import views
from .views import (
    CheckoutView,
    OrderSummaryView,
    OrderSummaryRawView,
    WishView,
    WishRawView,
    add_to_cart,
    add_to_wish,
    remove_from_cart,
    remove_from_wish,
    remove_single_item_from_cart,
    add_to_cart_category,
    add_single_item_from_cart,
    PaymentView,
)

app_name='shop'

urlpatterns = [
    path('',views.Home, name='index'),
    path('item/addcomment/<int:pk>/', views.addcomment, name='addcomment'),
    path('user-dashboard/', views.Dashboard, name="dashboard"),
    path('shop/', views.Shop, name='shop'),
    path('product-details/<int:pk>/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>/', views.product_detail_for_login, name='login-product-detail'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('add_to_cart_category/<int:pk>/', add_to_cart_category, name='add_to_cart_category'),
    path('order-summary/<int:pk>/',OrderSummaryView.as_view(), name="order-summary"),
    path('users-cart/',OrderSummaryRawView.as_view(), name="order-summary-raw"),
    path('wishlist/<int:pk>/', WishView.as_view(), name="wishlist"),
    path('wish-list/', WishRawView.as_view(), name="wishlist-raw"),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('add-to-wish/<int:pk>/', add_to_wish, name='add-to-wish'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-wish/<int:pk>/', remove_from_wish, name='remove-from-wish'),
    path('remove_single_item_from_cart/<int:pk>/', remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('add_single_item_to_cart/<int:pk>/', add_single_item_from_cart, name="add_single_item_from_cart"),
    

    #ORDER ESSENTIAL PAGES
    #path('gallery',views.gallery, name='gallery'),
    #path('contact',views.contact, name='contact'),
    #path('blog',views.blog, name='blog'),
    #path('blog_single',views.blog_single, name='blog-single'),
    #path('accomodation',views.accomodation, name='accomodation'),
    #path('about',views.about, name='about'),
    
]

