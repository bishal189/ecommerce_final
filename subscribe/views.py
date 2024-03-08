from django.http import JsonResponse
from Category.models import Category
from subscribe.models import SubscribeModel
from account.models import Account
# Create your views here.
def subscribe(request,category_id):
   try:
       user=request.user
       category=Category.objects.get(id=category_id)
       print(category)
       subscribed, created = SubscribeModel.objects.get_or_create(category=category)
       if created:
            subscribed.subscribers.add(user)
            print("created")
       else:
               print("not created")
       return JsonResponse({'message':"Category Subscribed"},status=200)
   except Exception as e:
        error=str(e)
        print(error)
        return JsonResponse({'error':f"unexcepcted error: {error}"},status=400)


def unsubscribe(request,category_id):
    try:
       user=request.user
       category=Category.objects.get(id=category_id)
       print(category)
       subscribed, created = SubscribeModel.objects.get_or_create(category=category)
       if created:
            subscribed.subscribers.add(user)
            print("created")
       else:
            print("not created")
       return JsonResponse({'message':"Category Subscribed"},status=200)
    except Exception as e:
        error=str(e)
        print(error)
        return JsonResponse({'error':f"unexcepcted error: {error}"},status=400)

