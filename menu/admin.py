from django.contrib import admin
from .models import MenuItem, MenuCategory, Restaurant

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(MenuCategory)
admin.site.register(Restaurant)
