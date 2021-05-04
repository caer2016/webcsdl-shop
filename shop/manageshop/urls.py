from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.ProductList, name = 'ManagerProductList'),
    path('products/<str:mode>', views.ProductList, name = 'ManagerProductListMode'),
    path('add/', views.AddProduct, name = 'ManagerAddProduct'),
    path('import/', views.AddImport, name = 'ManagerImportProduct'),
    path('orders/<str:mode>', views.OrderList, name = 'ManagerOrderList'),
    path('importorders/<str:mode>', views.ImportList, name = 'ManagerImportList'),
    path('importorders/delete/<int:id>', views.DeleteImport, name = 'ManagerDeleteImport'),
    path('confirm/<int:id>', views.ConfirmOrder, name = 'ManagerConfirmOrder'),
    path('cancel/<int:id>', views.CancelOrder, name = 'ManagerCancelOrder')
]