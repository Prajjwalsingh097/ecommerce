from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('home/', views.home),
    path('add_product/', views.add_product),
    path('product_addedd/', views.product_addedd),
    path('category/<int:id>/',views.category, name="category"),
    path('profile/',views.profile, name="profile"),
    


    
]