from django.urls import path, include

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="siteHome"),
    path('landing/', HomeView.as_view(), name="landingPage"),
    path('product/<int:prodid>', ProductView.as_view(),name='single-product'),
    path('cart',CartView.as_view(),name="cart"),
    path('checkout',Checkout.as_view(),name="checkout"),
    path('product_rating/',RatingProduct.as_view(),name="product_rating"),
    path('search/',SearchProduct.as_view(),name="search")
]
