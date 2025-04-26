from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/categories/', views.MenuCategoryListView.as_view(), name='menu-category-list'),
    path('menu-categories/<int:pk>/', views.MenuCategoryDetailView.as_view(), name='menu-category-detail'),
    path('menu-categories/<int:category_id>/items/', views.MenuItemListView.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('restaurants/<int:restaurant_id>/templates/', views.MenuTemplateListView.as_view(), name='menu-template-list'),
    path('menu-templates/<int:pk>/', views.MenuTemplateDetailView.as_view(), name='menu-template-detail'),
    path('restaurants/<int:restaurant_id>/qr/', views.QRCodeView.as_view(), name='qr-code'),
    path('qr_code/<int:restaurant_id>.png', views.qr_code_image_view, name='qr_code_image'),
]
