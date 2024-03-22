from django.http import JsonResponse
from Category.models import Category
from subscribe.models import SubscribeModel
from account.models import Account
# Create your views here.
def subscribe(request,category_id):
   try:
       user=request.user
       if request.user.is_authenticated==False:
            return JsonResponse({'error':"Sign in first"},status=400)
       category=Category.objects.get(id=category_id)
       print(category)
       subscribed, created = SubscribeModel.objects.get_or_create(category=category)
       subscribed.attach(user)
       return JsonResponse({'message':"Category Subscribed"},status=200)

   except Exception as e:
        error=str(e)
        print(error)
        return JsonResponse({'error':f"unexcepcted error: {error}"},status=400)


def unsubscribe(request,category_id):
    try:
       user=request.user
       if request.user.is_authenticated==False:
            return JsonResponse({'error':"Sign in first"},status=400)

       category=Category.objects.get(id=category_id)
       subscribed = SubscribeModel.objects.get(category=category)
       subscribed.detach(user)
       return JsonResponse({'message':"Category Unsubscribed"},status=200)
    except Exception as e:
        error=str(e)
        print(error)
        return JsonResponse({'error':f"unexcepcted error: {error}"},status=400)

