from django.contrib import admin
from django.urls import path, include

from .import views 

urlpatterns = [
    path('', views.index, name = 'index'),
    path('products/<str:filter>', views.ProductListView, name = 'ProductList'),
    path('products/details/<int:id>', views.ProductDetailView, name = 'ProductDetail')
]