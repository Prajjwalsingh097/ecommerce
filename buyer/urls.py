
from django.contrib import admin
from django.urls import path, include
from .import views


urlpatterns = [
    path('home/',views.home),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('category/<int:id>/',views.category, name="category"),
    path('cartDetails/',views.cartDetails,name="cartDetails"),
    path('cartdel/<int:id>/',views.cartdel,name="cartdel"),
    path('checkout/',views.checkout),
    path('profile/',views.profile, name="profile"),
    path('updateAddress/',views.updateAddress, name="updateAddress"),
    path('updateUserDetails/',views.updateUserDetails, name="updateUserDetails"),
    path('orders/',views.orderDetails),
    path('Order_by_id/<int:id>',views.Order_by_id,name="Order_by_id"),
    
    
    
    
    
    
]