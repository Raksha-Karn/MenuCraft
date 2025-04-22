from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from menu.models import MenuCategory, MenuItem, Restaurant, MenuTemplate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import RestaurantSerializer, MenuItemSerializer, MenuCategorySerializer, MenuTemplateSerializer


class AuthenticatedAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class RestaurantListView(AuthenticatedAPIView):
    def get(self, request):
        restaurants = Restaurant.objects.filter(owner=request.user)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailView(AuthenticatedAPIView):
    def get_object(self, request, pk):
        return get_object_or_404(Restaurant, pk=pk, owner=request.user)

    def get(self, request, pk):
        restaurant = self.get_object(request, pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurant = self.get_object(request, pk)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(request, pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuCategoryListView(AuthenticatedAPIView):
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
        categories = MenuCategory.objects.filter(restaurant=restaurant)
        serializer = MenuCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
        data = request.data.copy()
        data['restaurant'] = restaurant.id
        serializer = MenuCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuCategoryDetailView(AuthenticatedAPIView):
    def get_object(self, pk, user):
        category = get_object_or_404(MenuCategory, pk=pk)
        if category.restaurant.owner != user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        return category

    def get(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = MenuCategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = MenuCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuItemListView(AuthenticatedAPIView):
    def get(self, request, category_id):
        category = get_object_or_404(MenuCategory, pk=category_id)
        if category.restaurant.owner != request.user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        items = MenuItem.objects.filter(category=category)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, category_id):
        category = get_object_or_404(MenuCategory, pk=category_id)
        if category.restaurant.owner != request.user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['category'] = category.id
        serializer = MenuItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuItemDetailView(AuthenticatedAPIView):
    def get_object(self, pk, user):
        item = get_object_or_404(MenuItem, pk=pk)
        if item.category.restaurant.owner != user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        return item

    def get(self, request, pk):
        item = self.get_object(pk, request.user)
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk, request.user)
        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk, request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuTemplateListView(AuthenticatedAPIView):
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
        templates = MenuTemplate.objects.filter(restaurant=restaurant)
        serializer = MenuTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
        data = request.data.copy()
        data['restaurant'] = restaurant.id
        serializer = MenuTemplateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuTemplateDetailView(AuthenticatedAPIView):
    def get_object(self, pk, user):
        template = get_object_or_404(MenuTemplate, pk=pk)
        if template.restaurant.owner != user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        return template

    def get(self, request, pk):
        template = self.get_object(pk, request.user)
        serializer = MenuTemplateSerializer(template)
        return Response(serializer.data)

    def put(self, request, pk):
        template = self.get_object(pk, request.user)
        serializer = MenuTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        template = self.get_object(pk, request.user)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
