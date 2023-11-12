from django.shortcuts import render
from Product.models import Category, Product, ProductVariant
from .models import CarouselItem
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation


def home(request):
    featured_products = Product.objects.filter(product_status='published', featured=True).order_by('created_at')
    featured_products_variants = ProductVariant.objects.filter(featured=True).order_by('created_at')
    categories = Category.objects.all()
    carousel_list = CarouselItem.objects.filter(status='active').order_by('priority')
    context = {
        'carousel_list': carousel_list,
        "categories": categories,
        "featured_products": featured_products,
        "featured_products_variants": featured_products_variants,
    }
    return render(request, 'mainhome/mainhome.html', context)


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response
