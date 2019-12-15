from django.contrib import admin

from .models import (
    Product,
    Category,
    Subcategory,
    CartItem,
    WishlistItem,
    Order,
)

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Order)
