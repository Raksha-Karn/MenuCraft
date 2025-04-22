from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.RestaurantView.as_view(), name='restaurant'),
    path('menu-items/', views.MenuView.as_view(), name='menu'),
    path('menu-category/', views.MenuCategoryView.as_view(), name='menu-category'),
]
