
from django.urls import path
from . import views

urlpatterns = [
 
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_details,name='product_details'),
    path('search/',views.search,name='search'),
    path('range/',views.ranges,name='range'),
    path('submit_reveiw/<int:product_id>',views.submit_review,name='submit_review'),
    path('account/add_product/',views.add_product,name='add_product'),
]
