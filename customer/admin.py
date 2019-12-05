from django.contrib import admin

from .models import (
    User,
    Cart,
    Wishlist,
    SavedForLater,
)
# Register your models here.

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(SavedForLater)
