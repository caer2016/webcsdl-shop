from django.shortcuts import render
from main.models import *
from main.views import getSidebarInfo 

def ProductList(request, mode = 'name'):

    product_quantity_dict = {}
    product_list = Product.objects.all().order_by(mode)
    context = {'product_list' : product_list, **getSidebarInfo()}
    return render(request, 'manageshop/manager_product_list.html', context)

def AddProduct(request):

    if request.method == "POST":
        # ADD PRODUCT LOGIC
        return render(request, 'manageshop/manager_add_product.html', {'notif': 'Added product'})

    return render(request, 'manageshop/manager_add_product.html')

def OrderList(request, mode):

    pending_cart_list = CustomerCartOrder.objects.filter(shippedDate__isnull = True).order_by(mode)
    shipped_cart_list = CustomerCartOrder.objects.filter(shippedDate__isnull = False).order_by(mode)

    context = {'pending_cart_list' : pending_cart_list, 'shipped_cart_list' : shipped_cart_list}

    return render(request, 'manageshop/manager_order_list.html', context)

def ImportList(request, mode):
    
    import_list = ImportOrder.objects.all().order_by(mode)
    context = {'import_list' : import_list}

    return render(request, 'manageshop/manager_import_list.html', context)

def AddImport(request):

    if request.method == "POST":

        #CREATE IMPORT ORDER
        
        for key, value in request.POST.items():
            if key != 'crsfmiddlewaretoken':
                #ADD ITEM
                pass

        return render(request, 'manageshop/manager_add_import.html', {'notif': 'Added import order'})
    
    return render(request, 'manageshop/maanger_add_import.html')