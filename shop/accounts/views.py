from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from main.models import Customer, CartOrderIndividual, CustomerCartOrder
from main.views import getSidebarInfo

# Create your views here.
def register(request):
    
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            newuser = form.save()

            address = request.POST['address']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            newcustomer = Customer(user = newuser, address = address) 
            newcustomer.save()
            user = authenticate(username = username, password = password)

            login(request, user)
            return redirect('/products/all')

    else:
        form = UserCreationForm()

    context = { 'form': form } 
    return render(request, 'registration/register.html', context)

class cartData:

    def __init__(self, cart):
        self.id = cart.id
        self.orderDate = cart.orderDate
        
        self.items = []
        self.total = 0
        self.customer = cart.customer.user.username
        
        self.shipped = (cart.shippedDate != None)

        itemquery = CartOrderIndividual.objects.filter(cartOrder = cart)
        for item in itemquery:
            self.items.append(str(item.product.name) + ' x ' + str(item.quantity))
            self.total += item.quantity * item.product.unitPrice

def profile(request, *args):

    try:
        customer = request.user.customer
    except:
        raise Http404("Only customer can access this page")

    pending_cart = []
    for cart in CustomerCartOrder.objects.filter(orderDate__isnull = False, shippedDate__isnull=True):
        pending_cart.append(cartData(cart))

    context = {'customer': customer, 'notification' : args, 'pending_cart': pending_cart, **getSidebarInfo()}

    return render(request, 'registration/profile.html', context)

def profile_update(request):

    try:
        customer = request.user.customer
    except:
        raise Http404("Only customer can access this page")

    if request.method == 'POST':
        newaddress = request.POST['newaddress']
        customer.address = newaddress
        customer.save() 
        return redirect('profile', args=['Update successful'])

    return render(request, 'registration/profile_update.html', context)