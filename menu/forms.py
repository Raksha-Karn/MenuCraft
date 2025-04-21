from django import forms
from .models import Restaurant, MenuCategory, MenuItem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
