from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    opening_hours = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=50)
    price_range = models.CharField(max_length=50)
    rating = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='restaurant_images/')
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
