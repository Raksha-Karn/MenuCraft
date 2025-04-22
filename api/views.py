from django.shortcuts import render
from rest_framework.views import APIView
from menu.models import MenuCategory, MenuItem, Restaurant
from rest_framework.response import Response
from rest_framework import status
from .serializers import RestaurantSerializer, MenuItemSerializer, MenuCategorySerializer


class RestaurantView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
