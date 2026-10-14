from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from shop.models import Products

# Create your views here.
def getSimilarProducts(request,prodId):


    recommendationsJSON = generateSimilarRecommendations(prodId)

    return JsonResponse(recommendationsJSON,safe=False)



def getProductInfoByID(request,prodId):

    productModel = Products

    try:
        product_info = Products.objects.get(id=prodId)


        if(product_info is None):
            return JsonResponse({"success":False,"p_data" : {}},safe=False)

        else:
            return JsonResponse({"success": True, "p_data": {
                "id": product_info.id,
                "name": product_info.name,
                "price": product_info.price,
                "img_url":product_info.featured_img_url,
                "desc":product_info.description
            }}, safe=False)


    except:
        # If there is no product found
        return JsonResponse({"success": False, "p_data": {}}, safe=False)