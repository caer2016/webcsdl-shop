from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from main.models import Customer

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

def profile(request, *args):

    try:
        customer = request.user.customer
    except:
        raise Http404("Only customer can access this page")

    context = {'customer': customer, 'notification' : args}

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