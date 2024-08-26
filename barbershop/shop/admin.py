from django.contrib import admin
from .models import Product, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    list_filter = ['price', 'stock']
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'created_at', 'total']

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
