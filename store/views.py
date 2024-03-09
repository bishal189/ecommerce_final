from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product
from Category.models import Category
from cart.models import Cartitem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from cart.models import Order_Product
from .models import Product
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import models
from sentence_transformers import SentenceTransformer
from .utils import load_data,prepare_data


# for sematic search 


client = QdrantClient(":memory:")
client.recreate_collection(collection_name='product_collection',
                           vectors_config=models.VectorParams(
                               size=384, distance=models.Distance.COSINE
                           ))


# vectorized our data create word embedaded


model = SentenceTransformer('all-MiniLM-L6-v2')
df = load_data('/home/bishalm/Desktop/ecommerce/data1.csv')
docx, payload = prepare_data(df)




# vectors=load_vectors('vectorized_courses.pickle')
# print(docx)
vectors = model.encode(docx, show_progress_bar=True)


client.upload_collection(
    collection_name='product_collection',
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size=256

)





# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    



def store(request,category_slug=None):


    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        all_product=Product.objects.all().filter(is_available=True,category=categories)
        paginator=Paginator(all_product,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

        count=all_product.count()

    else:    

       all_product=Product.objects.all().filter(is_available=True).order_by('id')
       paginator=Paginator(all_product,6)
       page=request.GET.get('page')
       paged_products=paginator.get_page(page)

       count=all_product.count()
    context={
        'all_products':paged_products,
        'count':count,
        
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        



    except Exception as e:
    
        raise e;

    try:
        user=None
        if request.user.is_authenticated:
            user=request.user

        orders=Order_Product.objects.filter(user=user,product_id=single_product.id).exists()
        

    except Order_Product.DoesNotExist:

        orders=None 
    
    
    # get the reviews

    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)

    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'orders':orders,
        'reviews':reviews
    }        
    return render(request,'store/product_details.html',context);    







    
def search(request):
    if 'keyword'  in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            # products=Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            # count=products.count()
            # vectorized the search term
            vectorized_text = model.encode(keyword).tolist()
            products= client.search(collection_name='product_collection',
                        query_vector=vectorized_text, limit=5)
            # count=products.count()            
            #search the vectorDB and and get recomandation
            result=[]
            for product in products:
                if product.score>0.7:
                    data=Product.objects.get(id=product.payload['id'])
                    result.append(data)
        context={
            'all_products':result,
            'count':len(result)
        }    

    return render(request,'store/store.html',context)
    
# def search(request):
#     if 'keyword'  in request.GET:
#         keyword=request.GET['keyword']
#         if keyword:
#             products=Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
#             count=products.count()

#         context={
#             'all_products':products,
#             'count':count
#         }    

#     return render(request,'store/store.html',context)




def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            reveiws=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            
            # updating records
            form=ReviewForm(request.POST,instance=reveiws)
            form.save()
            messages.success(request,'Thanks you! your review has been updated')
            return redirect(url)




        except ReviewRating.DoesNotExist:
            print(request.POST)
            form=ReviewForm(request.POST)
            
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']

                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thanks you! your review has been submitted')
                return redirect(url)

             
