from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','currency')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','created_at','currency')
    inlines = [OrderItemInline]

admin.site.register(Discount)
admin.site.register(Tax)
