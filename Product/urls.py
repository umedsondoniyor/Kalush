from django.urls import path
from .views import *

urlpatterns = [
    path("", ProductList.as_view(), name="product_list"),
    path("product/<pid>", product_detail_view, name="product_detail"),
]
