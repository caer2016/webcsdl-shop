from django.shortcuts import render, redirect
from .models import Product

# Create your views here.
def index(request):
    return redirect('/products/all')

def ProductListView(request, filter : str):

    product_list = Product.objects.filter(productType = filter)
    context = {'product_list' : product_list}

    return render(request = request, template_name = 'product_list.html', context = context)