from django.shortcuts import render
from main.models import *
from main.views import getSidebarInfo 
from accounts.views import cartData

def ProductList(request, mode = 'name'):

    product_quantity_dict = {}
    product_list = Product.objects.all().order_by(mode)
    context = {'product_list' : product_list, **getSidebarInfo()}
    return render(request, 'manageshop/manager_product_list.html', context)

def AddProduct(request):

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        desc = request.POST['description']
        producttype = request.POST['type']
        image = request.FILES['imageUpload']

        product = Product.objects.create(name = name, unitPrice = price, image = image, productType = producttype, details = desc)
        product.save()

        return render(request, 'manageshop/manager_add_product.html', {'notif': 'Added product'})

    return render(request, 'manageshop/manager_add_product.html')

def OrderList(request, mode = 'all'):

    if mode=='pending':
        orders = CustomerCartOrder.objects.filter(shippedDate__isnull = True).order_by('orderDate')
    elif mode == 'shipped':
        orders = CustomerCartOrder.objects.filter(shippedDate__isnull = False).order_by('orderDate')
    else:
        orders = CustomerCartOrder.objects.all().order_by('orderDate')

    order_list = [] 
    for order in orders:
        order_list.append(cartData(order))

    context = {'order_list' : order_list}

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