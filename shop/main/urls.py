from django.contrib import admin
from django.urls import path, include

from .import views 

urlpatterns = [
    path('', views.index, name = 'index'),
    path('products/<str:filter>', views.ProductListView, name = 'ProductList'),
    path('products/details/<int:id>', views.ProductDetailView, name = 'ProductDetail'),
    path('cart', views.CartView, name = 'CartView'),
    path('checkout', views.Checkout, name = 'Checkout'),
    path('add/<int:id>', views.AddToCart, name = 'AddToCart'),
    path('cancel/<int:id>', views.CancelCart, name = 'cancel'),
]