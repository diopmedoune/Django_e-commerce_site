# accounts/admin.py

from django.contrib import admin

from store.models import Category, Product, Order, Cart, Souhait


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Souhait)