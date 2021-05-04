from django.shortcuts import render, redirect
from django.db.models import Count, Max
from .models import *
from django.http import Http404
from django.utils.timezone import now

# Create your views here.
def index(request):
    return redirect('/products/all')

def getSidebarInfo():
    product_type_list = Product.objects.values('productType').annotate(count = Count("productType")).order_by()
    all_products_count = len(Product.objects.all())

    return {'product_type_list': product_type_list, 'all_products_count': all_products_count}

def ProductListView(request, filter : str):

    if filter == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(productType = filter)
    
    if len(product_list) == 0:
        raise Http404("The type does not exist")

    header = filter.capitalize()

    context = {'product_list' : product_list, 'header' : header, **getSidebarInfo()}

    return render(request = request, template_name = 'product_list.html', context = context)

def ProductDetailView(request, id):

    product = Product.objects.get(id=id)
    review_list = Review.objects.filter(product = product)

    context = {'product': product, 'comment_list': review_list}

    return render(request, 'product_detail.html', context = context)


def getCart(user):

    customer = user.customer

    cart = CustomerCartOrder.objects.filter(customer = customer, orderDate__isnull = True).order_by('-id').first()
    if cart == None:
        cart = CustomerCartOrder.objects.create(customer = customer)

    return cart

def CartView(request):

    cart = CustomerCartOrder.objects.filter(customer = request.user.customer, orderDate__isnull = True).order_by('-id').first()
    orders = CartOrderIndividual.objects.filter(cartOrder = cart)

    if request.method == 'POST':

        for key, value in request.POST.items():
            if key!='csrfmiddlewaretoken':
                orderitem = orders.get(id = int(key))
                if int(value)==0:
                    orderitem.delete()
                else:
                    orderitem.quantity = int(value)
                    orderitem.save()

        # orders = CartOrderIndividual.objects.filter(cartOrder = cart)
        context = {'orders' : orders, 'updated_notif': True, **getSidebarInfo()}

        return render(request, 'cart_view.html', context = context)

    else:
        context = {'orders' : orders, 'updated_notif': False, **getSidebarInfo()}

        return render(request, 'cart_view.html', context = context)


def AddToCart(request, id):

    cart = getCart(request.user)
    product = Product.objects.get(id = id)
    quantity = request.POST['quantity']

    # if item is already in cart, add more to it
    existingItem = CartOrderIndividual.objects.filter(product = product, cartOrder = cart).first()
    if (existingItem == None):
        item = CartOrderIndividual.objects.create(product = product, quantity = quantity, cartOrder = cart)
        item.save() 
    else:
        existingItem.quantity += quantity
        existingItem.save()
    
    return redirect('ProductDetail', id)

def Checkout(request):

    cart = getCart(request.user)
    cart.orderDate = now()
    cart.save()

    return render(request, 'checkout.html')

def CancelCart(request, id):

    cart = CustomerCartOrder.objects.get(id = id)
    cart.delete()

    return redirect('profile')