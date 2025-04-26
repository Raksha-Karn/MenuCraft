from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework.views import APIView
from io import BytesIO
from menu.models import MenuCategory, MenuItem, Restaurant, MenuTemplate, QRCodeCustomization
from rest_framework.response import Response
import qrcode
import os
from django.conf import settings
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask
import base64
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import RestaurantSerializer, MenuItemSerializer, MenuCategorySerializer, MenuTemplateSerializer, QRCodeCustomizationSerializer


class AuthenticatedAPIView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
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

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_qr_code(restaurant_id, customization):
    menu_url = "" # to be implemented in frontend

    fill_color = hex_to_rgb(customization.qr_code_color)
    back_color = hex_to_rgb(customization.qr_code_background_color)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=customization.qr_code_size // 25,
        border=4,
    )

    qr.add_data(menu_url)
    qr.make(fit=True)

    module_drawer = None
    if customization.qr_code_module_drawer == 'rounded':
        module_drawer = RoundedModuleDrawer()
    elif customization.qr_code_module_drawer == 'circle':
        module_drawer = CircleModuleDrawer()

    color_mask = None
    if customization.qr_code_color_mask == 'radial':
        color_mask = RadialGradiantColorMask(
            back_color=back_color,
            center_color=fill_color,
            edge_color=fill_color
        )
    elif customization.qr_code_color_mask == 'linear':
        color_mask = SquareGradiantColorMask(
            back_color=back_color,
            center_color=fill_color,
            edge_color=fill_color
        )

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=color_mask,
        fill_color=fill_color,
        back_color=back_color,
    )

    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_code_dir, exist_ok=True)

    file_name = f"qr_code_{restaurant_id}.png"
    file_path = os.path.join(qr_code_dir, file_name)
    img.save(file_path, format="PNG")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return {
        'image_data': f"data:image/png;base64,{img_str}",
        'url': menu_url,
        'image_url': f"{settings.MEDIA_URL}qr_codes/{file_name}"
    }


class QRCodeView(AuthenticatedAPIView):
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)

        template = MenuTemplate.objects.filter(restaurant=restaurant).first()
        if not template:
            return Response({'detail': 'Menu template not found'}, status=status.HTTP_404_NOT_FOUND)

        qr_customization = QRCodeCustomization.objects.filter(template=template).first()
        if not qr_customization:
            qr_customization = QRCodeCustomization.objects.create(template=template)

        qr_code = generate_qr_code(restaurant_id, qr_customization)

        return Response({
            'qr_code': qr_code,
            'customization': QRCodeCustomizationSerializer(qr_customization).data
        })

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)

        template = MenuTemplate.objects.filter(restaurant=restaurant).first()
        if not template:
            return Response({'detail': 'Menu template not found'}, status=status.HTTP_404_NOT_FOUND)

        qr_customization, created = QRCodeCustomization.objects.get_or_create(template=template)

        serializer = QRCodeCustomizationSerializer(qr_customization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            qr_code = generate_qr_code(restaurant_id, qr_customization)

            return Response({
                'qr_code': qr_code,
                'customization': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def qr_code_image_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    template = MenuTemplate.objects.filter(restaurant=restaurant).first()
    if not template:
        return HttpResponse("Menu template not found", status=404)

    qr_customization = QRCodeCustomization.objects.filter(template=template).first()
    if not qr_customization:
        qr_customization = QRCodeCustomization.objects.create(template=template)

    file_name = f"qr_code_{restaurant_id}.png"
    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    file_path = os.path.join(qr_code_dir, file_name)

    generate_qr_code(restaurant_id, qr_customization)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
    else:
        return HttpResponse("QR code generation failed", status=500)
