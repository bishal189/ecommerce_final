from django.shortcuts import render,redirect,HttpResponse
from store.models import Product
from .models import Cart,Cartitem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Variation
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from.models import Order
import datetime
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage
from .models import Payment,Order_Product
from django.template.loader import render_to_string
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    





def add_cart(request,product_id):
    # if the user is login 
    current_user=request.user
     
    product=Product.objects.get(id=product_id) #get the particular product
    if current_user.is_authenticated:
        product_variation=[]
        if request.method == "POST":
            for item in request.POST:
                key=item;
                value=request.POST[key]
                
                try:
                    variation=Variation.objects.get(variation_category__iexact=key,variation_value__iexact=value)
                    # print(variation)
                    product_variation.append(variation)
                except:
                    pass    
            

        # now add the product in the cart   

        is_cart_item_exist=Cartitem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exist:
            cart_item=Cartitem.objects.filter(product=product,user=current_user)

            # if that product exist than which variation exist of that product
            # checking the variation of the quantity



            # we need three things

            #existiong variation->from database
            #current variation_->from product variation
            #item_id->database
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            # print(ex_var_list)
            if product_variation in ex_var_list:
            #   increase the cart item quantity
                index=ex_var_list.index(product_variation)
                
                item_id=id[index]
                
            

                item=Cartitem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()

            else:
                
                item=Cartitem.objects.create(product=product,quantity=1,user=current_user)
                if(len(product_variation))>0:
                    
                  item.variations.clear()
                  item.variations.add(*product_variation)
                item.save()    
            
            
    



        
        
            # cart_item.quantity=cart_item.quantity+1;
            

        else :

            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                user=current_user
            )
            if(len(product_variation))>0:
              cart_item.variations.clear()
              cart_item.variations.add(*product_variation)

            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        return redirect('cart');   
    else:
        # if the user is not login
        product_variation=[]
        if request.method == "POST":
            for item in request.POST:
                key=item;
                value=request.POST[key]
                
                try:
                    variation=Variation.objects.get(variation_category__iexact=key,variation_value__iexact=value)
                    # print(variation)
                    product_variation.append(variation)
                except:
                    pass    
            

            
    







    
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using the cart_id present in the session


        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )   

        cart.save()  




        # now add the product in the cart   

        is_cart_item_exist=Cartitem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exist:
            cart_item=Cartitem.objects.filter(product=product,cart=cart)

            # if that product exist than which variation exist of that product
            # checking the variation of the quantity



            # we need three things

            #existiong variation->from database
            #current variation_->from product variation
            #item_id->database
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            # print(ex_var_list)
            if product_variation in ex_var_list:
            #   increase the cart item quantity
                index=ex_var_list.index(product_variation)
                
                item_id=id[index]
                
            

                item=Cartitem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()

            else:
                
                item=Cartitem.objects.create(product=product,quantity=1,cart=cart)
                if(len(product_variation))>0:
                    
                  item.variations.clear()
                  item.variations.add(*product_variation)
                item.save()    
            
            
    



        
        
            # cart_item.quantity=cart_item.quantity+1;
            

        else :

            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                cart=cart,
            )
            if(len(product_variation))>0:
              cart_item.variations.clear()
              cart_item.variations.add(*product_variation)

            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        return redirect('cart');   




    
def cart(request,total=0,quantity=0,cart_items=None):
    
   
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
        

        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
       

        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity

        tax=(2*total)/100
        grand_total=total+tax;    


    except ObjectDoesNotExist:
        pass    
    

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'store/cart.html',context)



def remove_item(request,product_id,cart_item_id):
   
    product=Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Cartitem.objects.get(product=product,id=cart_item_id,user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))   
            cart_item=Cartitem.objects.get(product=product,id=cart_item_id,cart=cart) 
        if cart_item.quantity>1:
           cart_item.quantity-=1;
           cart_item.save()

        else:    
            cart_item.delete()


    except:
        pass
    return redirect('cart')    

def remove_cart_item(request,product_id,cart_item_id):
   
    product=Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
           cart_item=Cartitem.objects.get(user=request.user,product=product,id=cart_item_id)
        else:
           cart=Cart.objects.get(cart_id=_cart_id(request))
           cart_item=Cartitem.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item:
         cart_item.delete()
    except:
        pass



    return redirect('cart')    

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
     
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
        

        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
       


        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity

        tax=(2*total)/100
        grand_total=total+tax;    


    except ObjectDoesNotExist:
        pass    
    
    
    if request.method == "POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=request.user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.order_note=form.cleaned_data['order_note']
            data.total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()




            # generating order number


            yr=int(datetime.date.today().strftime("%Y"))
            dt=int(datetime.date.today().strftime("%d"))
            mt=int(datetime.date.today().strftime("%m"))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+ str(data.id)
            data.order_number=order_number
            data.save()







            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'grand_total':grand_total,
                 'tax':tax,
                 'total':total,

            }


            return render(request,'orders/payements.html',context)



        else:
            return redirect('checkout')    
            
    else:
        form=OrderForm()

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'form':form
    }
    return render(request,'store/checkout.html',context)



















def payement(request):
    
    body=json.loads(request.body)
    
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
 

    # store all the information in the payemnt model
    payment=Payment.objects.create(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payement_method'],
        amount_paid=order.total,
        status=body['status'],



    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()



# move the cart items to order product

    cart_items=Cartitem.objects.filter(user=request.user)
    
    for item in cart_items:
        print(item)
        orderproduct=Order_Product()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product.id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.is_ordered=True
        orderproduct.save()
        


        # for adding variation in that  particular item

        cart_item=Cartitem.objects.get(id=item.id)
        product_variation=cart_item.variations.all()
        orderproduct=Order_Product.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


# reduce the quantity of sold products
       
        product_item=Product.objects.get(id=item.product.id)
        product_item.stock-=item.quantity
        product_item.save()







# clear the cart

#  after payement sucessfull the cartitem in the cart should be clear
    Cartitem.objects.filter(user=request.user).delete()






# send order recived email to customer
# now sending the email to the user after the transactions sucessful
    # mail_subject='Thank you for your order!'
    # message=render_to_string('orders/order_recieved_email.html', {
    #     'user':request.user,
    #     'order':order
    # })


    # to_email=request.user.email
    # send_email=EmailMessage(mail_subject,message,to=[to_email])
    # send_email.send()












# send order number and transcation id back to senddata method via json response

    data={
        'order_number':order.order_number,
        'transID':payment.payment_id

    }

    return JsonResponse(data)





























    return render(request,'orders/payements.html')











def order_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
   
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=Order_Product.objects.filter(order_id=order.id)
        payement=Payment.objects.get(payment_id=transID)
        

        subtotal=0
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity;

        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':transID,
            'payment':payement,
            'subtotal':subtotal,
          
        }
        return render(request,'orders/order_complete.html',context)


    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
         
   