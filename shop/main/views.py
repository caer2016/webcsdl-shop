from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *
from django.http import Http404

# Create your views here.
def index(request):
    return redirect('/products/all')

def ProductListView(request, filter : str):

    if filter == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(productType = filter)
    
    if len(product_list) == 0:
        raise Http404("The type does not exist")

    product_type_list = Product.objects.values('productType').annotate(count = Count("productType")).order_by()
    all_products_count = len(Product.objects.all())
    header = filter.capitalize()

    context = {'product_list' : product_list, 'product_type_list' : product_type_list, 'all_products_count' : all_products_count, 'header' : header}

    return render(request = request, template_name = 'product_list.html', context = context)

def ProductDetailView(request, id):

    product = Product.objects.get(id=id)
    review_list = Review.objects.filter(product = product)

    context = {'product': product, 'comment_list': review_list}

    return render(request, 'product_detail.html', context = context)