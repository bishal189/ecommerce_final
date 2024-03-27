from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from store.models import Product
from django.shortcuts import render, redirect



def share_facebook(request, pk):
    product = get_object_or_404(Product, pk=pk)
    share_url = request.build_absolute_uri(reverse('product_details',  kwargs={'category_slug': product.category.slug, 'product_slug': product.slug}))
    # Redirect user to Facebook sharing dialog
    return redirect(f'https://www.facebook.com/sharer/sharer.php?u={share_url}')