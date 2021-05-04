from django.shortcuts import render, redirect
from main.models import *
from main.views import getSidebarInfo 
from accounts.views import cartData
from django.utils.timezone import now

def ProductList(request, mode = 'name'):

    if not request.user.is_staff:
        return redirect('index')

    product_quantity_dict = {}
    product_list = Product.objects.all().order_by(mode)
    context = {'product_list' : product_list, **getSidebarInfo()}
    return render(request, 'manageshop/manager_product_list.html', context)

def AddProduct(request):
    if not request.user.is_staff:
        return redirect('index')

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
    if not request.user.is_staff:
        return redirect('index')

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

def ConfirmOrder(request, id):
    if not request.user.is_staff:
        return redirect('index')

    order = CustomerCartOrder.objects.get(id = id)
    order.shippedDate = now()
    order.save()

    return redirect('ManagerOrderList', all)

def CancelOrder(request, id):
    if not request.user.is_staff:
        return redirect('index')

    order = CustomerCartOrder.objects.get(id = id)
    order.delete()

    return redirect('ManagerOrderList', all)

class importData:

    def __init__(self, importcart):
        self.id = importcart.id
        self.arrivedDate = importcart.arrivedDate
        self.vendor = importcart.vendor
        self.price = importcart.vendorPrice

        self.items = []
        itemquery = ImportOrderIndividual.objects.filter(importOrder = importcart)
        for item in itemquery:
            self.items.append(str(item.product.name + ' x ' + str(item.quantity)))

def ImportList(request, mode):
    if not request.user.is_staff:
        return redirect('index')
    
    imports = ImportOrder.objects.all().order_by(mode)
    
    import_list = []
    for importorder in imports:
        import_list.append(importData(importorder))

    context = {'import_list' : import_list}

    return render(request, 'manageshop/manager_import_list.html', context)

def DeleteImport(request, id):
    if not request.user.is_staff:
        return redirect('index')

    importorder = ImportOrder.objects.get(id=id)
    importorder.delete()
    return redirect('ManagerImportList', 'arrivedDate')

def AddImport(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == "POST":

        vendor = request.POST['vendor']
        vendorPrice = request.POST['vendorPrice']
        importorder = ImportOrder.objects.create(vendor = vendor, vendorPrice = vendorPrice)
        importorder.save()
        
        for key, value in request.POST.items():
            if value != 0 and key not in ['csrfmiddlewaretoken', 'vendor', 'vendorPrice']:
                product = Product.objects.get(id = int(key))
                item = ImportOrderIndividual.objects.create(importOrder = importorder, product = product, quantity = int(value))
                item.save()

        context = {'product_list' : Product.objects.all().order_by('name'), 'notif': 'Added import order'}

        return render(request, 'manageshop/manager_add_import.html', context)
    
    context = {'product_list' : Product.objects.all().order_by('name')}
    return render(request, 'manageshop/manager_add_import.html', context)