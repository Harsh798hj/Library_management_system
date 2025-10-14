from django.contrib import admin
from .models import User, Book, CartItem, IssuedBook, SavedForLater

admin.site.register(User)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(IssuedBook)
admin.site.register(SavedForLater)
