from os import read
from rest_framework import serializers
from menu.models import MenuCategory, MenuItem, Restaurant, MenuTemplate
from idlelib.idle_test.test_config import usercfg


class MenuTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuTemplate
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    categories = MenuCategorySerializer(many=True, read_only=True)
    templates = MenuTemplateSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        owner = self.context['request'].user
        return Restaurant.objects.create(owner=owner, **validated_data)
