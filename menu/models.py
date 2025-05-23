from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    owner = models.ForeignKey(User, related_name='restaurants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    opening_hours = models.CharField(max_length=100)
    closing_hours = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return str(self.name)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    is_vegetarian = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class MenuTemplate(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, related_name='templates', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    text_color = models.CharField(max_length=7, default='#000000')
    accent_color = models.CharField(max_length=7, default='#e45826')
    font_family = models.CharField(max_length=100, default='Playfair Display')
    logo_position = models.CharField(max_length=20, default='top',
                                   choices=[('top', 'Top'), ('left', 'Left'), ('none', 'None')])
    template_type = models.CharField(max_length=20, default='standard',
                                   choices=[('standard', 'Standard'), ('elegant', 'Elegant'),
                                            ('casual', 'Casual'), ('modern', 'Modern')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class QRCodeCustomization(models.Model):
    template = models.ForeignKey(MenuTemplate, related_name='customizations', on_delete=models.CASCADE)
    qr_code_size = models.PositiveIntegerField(default=200)
    qr_code_color = models.CharField(max_length=7, default='#000000')
    qr_code_background_color = models.CharField(max_length=7, default='#FFFFFF')
    qr_code_module_drawer = models.CharField(max_length=20, default='rounded',
                                             choices=[('rounded', 'Rounded'), ('circle', 'Circle')])
    qr_code_color_mask = models.CharField(max_length=20, default='radial',
                                          choices=[('radial', 'Radial'), ('linear', 'Linear')])

    def __str__(self):
        return f"{self.template.restaurant.name} - {self.template.name} - QR Code Customization"
