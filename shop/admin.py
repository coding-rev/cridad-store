from django.contrib import admin
from .models import Item, OrderItem, Order, Comment, Billingshop, Category

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title','brand','category','price','discount','photo')

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment','status', 'create_at']
    list_filter = ['status']
    random_fields = ('subject', 'comment', 'ip', 'user', 'item', 'rate')


admin.site.site_header = 'Cridad Cpanel'
admin.site.site_title = 'Cridad Cpanel'

#How to unregister Default fields( Eg: Group)
from django.contrib.auth.models import Group
admin.site.unregister(Group)


# Register your models here.
admin.site.register(Comment, CommentAdmin),
admin.site.register(Category),
admin.site.register(Item, ItemAdmin),
admin.site.register(OrderItem),
admin.site.register(Order),

