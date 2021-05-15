
from django.contrib import admin
from django.urls import path, include
from .import views


urlpatterns = [
    path('home/',views.home),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('category/<int:id>/',views.category, name="category"),
    path('cart/',views.cartDetails,name="cart"),
    
    
]