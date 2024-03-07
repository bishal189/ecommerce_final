from django.contrib import admin
from .models import Product,Variation,ReviewRating

# Register your models here.


class Store_Admin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['product_name'],
    }
    list_display=('product_name','price','stock','category','modified_at','is_available')
    list_display_links=('product_name','price','stock','category','modified_at','is_available')

class variation_admin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','created_date','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')

admin.site.register(Product, Store_Admin)
admin.site.register(Variation,variation_admin)
admin.site.register(ReviewRating)