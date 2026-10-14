from django.urls import path, include

from .views import *

urlpatterns = [
    path('gen_recommendations/<int:prodId>',getSimilarProducts,name="getRecommendations"),
    path('get_product_by_id/<int:prodId>',getProductInfoByID, name="getProductById")
]
