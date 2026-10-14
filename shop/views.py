from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from shop.models import Products, Orders, OrderLineItems ,Rating
from django.contrib.auth.models import User
from user_control.models import UsersAccount
import json
import pprint
import math

class HomeView(TemplateView):

    template_name = "homepage/home.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        products = Products.objects.all().order_by('name')

        data = {
            "products":products,
            "page_title":self.page_title
        }


        # Calculate Cart Length
        if ("cart" in request.session):
            data["cart"] = request.session["cart"]
            # Calculate Current Cart Length
            cartlength = 0
            if (isinstance(request.session["cart"], (tuple, list))):
                cartlength = len(request.session["cart"])
            if (isinstance(request.session["cart"], dict)):
                cartlength = 1
            data["cartlength"] = cartlength
            
        response = TemplateResponse(request,self.template_name, data)
        return response



class ProductView(TemplateView):

    template_name = "single-product/template.html"


    def get(self,request,prodid):

        # product_id = self.kwargs['prodid']

        product = Products.objects.get(id=prodid)

        page_title = product.name + " | MorningShop"

        # request.session['cart'] = ({"id": 4, "q": 1},{"id":5,"q":12})

        isLoggedIn = False

        if(request.user.id):
            isLoggedIn = True

        data = {
            "products":product,
            "page_title": page_title,
            "isLoggedIn":isLoggedIn
        }

        if("cart" in request.session):
            data["cart"] = request.session["cart"]

            # Calculate Current Cart Length
            cartlength = 0
            if(isinstance(request.session["cart"], (tuple,list))):
                cartlength = len(request.session["cart"])
            if(isinstance(request.session["cart"], dict)):
                cartlength = 1
            data["cartlength"] = cartlength


        # data["notification"] = { "message":"The Product has been successfully added to your Cart.", "type":"success" }
        # print(cartlength)
        response = TemplateResponse(request,self.template_name, data)
        return response


    def post(self,request,prodid):
        # product_id = self.kwargs['prodid'

        product = Products.objects.get(id=prodid)

        page_title = product.name + " | MorningShop"

        # if('cart' in request.session) {
        #     request.session['cart'].append()
        # } else {
        #
        # }

        data = {
            "products": product,
            "page_title": page_title,
        }


        # Adding product to Cart

        quantity = request.POST['quantity']
        product_to_add = request.POST['product_id'];

        # request.session["cart"] = []

        # print(isinstance(request.session["cart"], dict))

        if('cart' in request.session):
            cart = request.session['cart']
        else :
            request.session["cart"] = []
            cart = request.session["cart"]

        # print(cart)
        if (cart):
            # print(type(cart))
            if (isinstance(cart, dict)):

                request.session['cart'] = [{"id": product_to_add, "q": quantity}, cart]
            elif (isinstance(cart, (tuple,list))):
                cart = list(cart)
                cart.append({"id": product_to_add, "q": quantity})

                request.session['cart'] = tuple(cart)
        else:
            request.session['cart'] = [{"id": product_to_add, "q": quantity}]

        if ("cart" in request.session):
            data["cart"] = request.session["cart"]

            # Calculate Current Cart Length
            cartlength = 0
            if (isinstance(request.session["cart"], (tuple, list))):
                cartlength = len(request.session["cart"])
            if (isinstance(request.session["cart"], dict)):
                cartlength = 1
            data["cartlength"] = cartlength

        data["notification"] = { "message":"The Product has been successfully added to your Cart.", "type":"success" }

        response = TemplateResponse(request, self.template_name, data)
        return response

class CartView(TemplateView):

    template_name = 'cart/template.html'

    def get(self,request):

        data = {
            "cartData": []
        }

        totalOrderValue = 0
        # print(request.session["cart"])
        if ("cart" in request.session):
            for cartitem in request.session["cart"]:
                print(cartitem)
                cartProduct = Products.objects.get(id = cartitem["id"])

                productStructured = {
                    "name" : cartProduct.name,
                    "price": cartProduct.price,
                    "quantity": cartitem["q"],
                    "total": int(cartProduct.price) * int(cartitem["q"]),
                    "featured_img": cartProduct.featured_img_url
                }

                data["cartData"].append(productStructured)

                totalOrderValue = totalOrderValue + productStructured["total"]


        else:
            data["cartData"] = []

        data["totalOrderValue"] = totalOrderValue
        # print(len(data["cartData"]))


        # For cart data in Javascript Variable
        if ("cart" in request.session):
            data["cart"] = request.session["cart"]

        response = TemplateResponse(request,self.template_name,data)

        return response

    def post(self,request):

        if("cart" in request.session):
            del request.session["cart"]

        return redirect("cart")



class Checkout(TemplateView):
    template_name = "checkout/template.html"

    def get(self, request):

        data = {
            "cartData": []
        }

        totalOrderValue = 0
        # print(request.session["cart"])

        if ("cart" in request.session):
            mainCart = request.session["cart"]
            cartlength = mainCart
        else:
            return redirect("siteHome")



        # For cart data in Javascript Variable
        if ("cart" in request.session):
            data["cart"] = request.session["cart"]



        if ("cart" in request.session):
            for cartitem in request.session["cart"]:

                cartProduct = Products.objects.get(id = cartitem["id"])

                productStructured = {
                    "name" : cartProduct.name,
                    "price": cartProduct.price,
                    "quantity": cartitem["q"],
                    "total": int(cartProduct.price) * int(cartitem["q"]),
                    "featured_img": cartProduct.featured_img_url
                }

                data["cartData"].append(productStructured)

                totalOrderValue = totalOrderValue + productStructured["total"]


        else:
            data["cartData"] = []



        # Adding user data for checkout page
        currentUser = UsersAccount.objects.get(mainUser = request.user)


        userData = {
            "name": currentUser.mainUser.first_name,
            "lname":currentUser.mainUser.last_name,
            "phone": currentUser.Phone,
            "email": currentUser.mainUser.email,
            "country":currentUser.Country,
            "addr_1": currentUser.Address,
            "addr_2":"",
            "city": currentUser.City,
            "district":currentUser.City,
            "zip_code": currentUser.zipCode,
        }

        data["userData"] = userData

        data["cartTotal"] = totalOrderValue
        # print(len(data["cartData"]))

        response = TemplateResponse(request,self.template_name,data)

        return response

    def post(self, request):
        if request.user.is_authenticated == False:
              return 1
    # Variable to hold users data
        orderUser = {
            "name":"",
            "lname": "",
            "phone": "",
            "email": "",
            "country": "",
            "addr_1": "",
            "addr_2": "",
            "city": "",
            "district":"",
            "zip_code":"",
        }

        if('name' in request.POST):
            orderUser['name'] = request.POST['name']

        if ('lname' in request.POST):
            orderUser['lname'] = request.POST['lname']

        if ('phone' in request.POST):
            orderUser['phone'] = request.POST['phone']

        if ('email' in request.POST):
            orderUser['email'] = request.POST['email']

        if ('country' in request.POST):
            orderUser['country'] = request.POST['country']

        if ('addr_1' in request.POST):
            orderUser['addr_1'] = request.POST['addr_1']

        if ('addr_2' in request.POST):
            orderUser['addr_2'] = request.POST['addr_2']

        if ('city' in request.POST):
            orderUser['city'] = request.POST['city']

        if ('district' in request.POST):
            orderUser['district'] = request.POST['district']

        if ('zip_code' in request.POST):
            orderUser['zip_code'] = request.POST['zip_code']


        generateOrder = Orders()

        generateOrder.shipping_name = orderUser['name']  + orderUser['lname']
        generateOrder.shipping_phone = orderUser['phone']
        generateOrder.shipping_email = orderUser['email']
        generateOrder.shipping_city = orderUser['city']
        generateOrder.shipping_country = orderUser['country']
        generateOrder.shipping_addr_1 = orderUser['addr_1']
        generateOrder.shipping_addr_2 = orderUser['addr_2']
        generateOrder.shipping_district = orderUser['district']
        generateOrder.shipping_zip = orderUser['zip_code']
        generateOrder.total = 0
        generateOrder.orderCustomer = UsersAccount.objects.get(mainUser=request.user)
        generateOrder.save()

        generatedOrder = generateOrder.id

        # Calculating Cart Data
        totalOrderValue = 0

        empty_cart = False

        if ("cart" in request.session):
            for cartitem in request.session["cart"]:
                cartProduct = Products.objects.get(id=cartitem["id"])

                order_item = OrderLineItems()

                order_item.order_id = generateOrder
                order_item.product_id =  cartProduct
                order_item.quantity = cartitem["q"]

                order_item.save()


                # data["cartData"].append(productStructured)

                totalOrderValue = totalOrderValue + int(cartProduct.price) * int(cartitem["q"])
        else:
            empty_cart = True

        if(empty_cart is False):
            mainOrder = Orders.objects.get(id=generatedOrder)
            mainOrder.total = totalOrderValue
            mainOrder.save()

            endResponse = {
                "add_order":True,
                "success":True,
                "order_id": generatedOrder
            }

            del request.session['cart']

        else:
            endReponse = {
                "add_order": True,
                "success": False,
                "message":""
            }

        response = TemplateResponse(request, self.template_name, {"order_id":16,"success":True,"add_order":True})

        return response

# this section product rating system plz do not miss it
class RatingProduct(TemplateView):
    template_name = "user/user_home.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def post(self,request):
        currentuser = request.POST['user_id']
        rating_star = request.POST['rating_star']
        product_id = request.POST.get('product_id',False)
        Data = Rating(user_id = currentuser,product_id = product_id,rating = rating_star)
        Data.save()

        Rating_filter  = Rating.objects.filter( product_id = product_id)
        i=0
        total_rates = 0
        for rate in Rating_filter:
            total_rates = total_rates + rate.rating
            i =  i + 1

        calculatedRating = math.floor(total_rates / i)

        ProductToUpdate = Products.objects.get(id=product_id)

        ProductToUpdate.rating = calculatedRating

        ProductToUpdate.save()

        return redirect('/product/'+product_id)

    def get(self,request):
        return redirect('/shop/landing/')


class SearchProduct(TemplateView):

    template_name = 'search-results/template.html'


    def get(self,request):

        if("search_term" in request.GET and request.GET["search_term"] != ''):
            term = request.GET['search_term']
        else:
            term = False

        if(term is not False):
            searchResultProducts = Products.objects.filter(name__icontains=term )
        else:
            searchResultProducts = list()

        if(term is not False and len(searchResultProducts) > 0):
            pageTitle = "Search results for " + term
        else:
            pageTitle = "Nothing Found"

        data = {
            "searchTerm" : term,
            "page_title": pageTitle,
            "products": searchResultProducts,
            "number_of_products" : len(searchResultProducts)
        }

        return TemplateResponse(request,self.template_name,data)