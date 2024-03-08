from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from store.models import Product
from Category.models import Category
from cart.models import Cartitem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from cart.models import Order_Product
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
        context={
        'all_products':paged_products,
        'category':True,
        'category_id':categories.id,
        'count':count,

    }

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





def semantic_search(query):
    # Preprocess query using spaCy
    query_doc = SPACY_NLP(query)
    
    # Search products using semantic similarity
    products = Product.objects.all()
    relevant_products = []
    for product in products:
        product_doc = SPACY_NLP(product.description)
        similarity_score = query_doc.similarity(product_doc)
        if similarity_score > 0.5:  # Adjust threshold as needed
            relevant_products.append(product)

    print(relevant_products)        
    
    return relevant_products


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Perform semantic search
            relevant_products = semantic_search(keyword)
            count = len(relevant_products)
            context = {
                'all_products': relevant_products,
                'count': count,
                'search_query': keyword
            }
    return render(request, 'store/store.html', context)

# def search(request):
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
#         if keyword:
#             # Perform semantic search
#             relevant_products = semantic_search(keyword)
#             count = len(relevant_products)
#         else:
#             relevant_products = []
#             count = 0
#     else:
#         relevant_products = Product.objects.all()
#         count = relevant_products.count()

#     context = {
#         'all_products': relevant_products,
#         'count': count
#     }

#     return render(request, 'store/store.html', context)



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



