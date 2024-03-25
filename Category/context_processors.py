


from .models import Category

def links(request):
    links_category=Category.objects.all().order_by('-id')
    print(links)
    return {'links': links_category}
