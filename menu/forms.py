from django import forms
from .models import Restaurant, MenuCategory, MenuItem, MenuTemplate

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


class MenuTemplateForm(forms.ModelForm):
    class Meta:
        model = MenuTemplate
        fields = '__all__'
