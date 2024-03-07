from django.http import response,HttpResponse
from django.shortcuts import render
from store.models import Product

def home(request):
     
    product_all=Product.objects.filter(is_available=True)
    # print(product_all)
    context={
        'all_product':product_all,
    }

    return render(request,'home.html',context)
