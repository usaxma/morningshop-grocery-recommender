from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from .models import UsersAccount
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
import pprint
from shop.models import Products as ProductModel, Orders, OrderLineItems ,Rating
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage

class UserHome(TemplateView):
    template_name = "user/user_home.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."
    def get(self,request):
        # auth Module Begin
        currentuser = request.user
        userAccess = restrictUserAccess(currentuser,'customer')
        if(userAccess != True):
            return userAccess
        # Auth Module End
        context = {'Products': ProductModel.objects.all()}
        return TemplateResponse(request,self.template_name,context)
    

@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(TemplateView):
    template_name = "user/user_login.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."
    
    def get(self,request):
        return TemplateResponse(request,self.template_name)

    def post(self, request):

        Email = request.POST['Email']
        Password = request.POST['Password']

        verifyUser = authenticate(request, username=Email,password=Password)

        if(verifyUser is not None):

            login(request, verifyUser)
            
            userProfileData = UsersAccount.objects.get(mainUser=verifyUser)
            
            if(userProfileData.account_type == 'admin'):
                if(userProfileData.status == 1):
                    request.session['login_flag'] = 1
                    request.session['user_id'] = verifyUser.id
                    return redirect('admin_dashboard')
                else:

                    return TemplateResponse(request, self.template_name,{'error': 'This User is Not Activated Plase contact to admin'})

            elif(userProfileData.account_type == 'customer'):
                if(userProfileData.status == 1):
                    request.session['Email'] =  Email
                    request.session['login_flag'] = 2
                    request.session['user_id'] = verifyUser.id
                    return redirect('siteHome')
                else:

                    return TemplateResponse(request, self.template_name,{'error': 'This User is Not Activated Plase contact to admin'})

            return False
        else:
            return TemplateResponse(request, self.template_name,{'error': 'Email or Password is Wrong'})


class UserSignUp(TemplateView):
    template_name = "user/user_signup.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        return TemplateResponse(request,self.template_name)
   
    def post(self,request):
        Email = request.POST['Email']
        Password = request.POST['Password']
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        Gender = request.POST['Gender']
        DateOfBirth = request.POST['DateOfBirth']
        Phone = request.POST['Phone']
        Address = request.POST['Address']
        City = request.POST['City']
        Country = request.POST['Country']
        zipCode  = request.POST['zipCode']
        account_type  = 'customer'
        status = 0

        user_exists = User.objects.all().filter(username  = Email)


        if(user_exists):
            return TemplateResponse(request, self.template_name, {'error': 'User with this email already exists.'})

        newuser = User.objects.create_user(Email,Email,Password)
        newuser.first_name = FirstName
        newuser.last_name = LastName

        newuser.save()


        try:
            userdetail = User.objects.get(username = Email)

            Data = UsersAccount(mainUser = userdetail, Gender = Gender, DateOfBirth = DateOfBirth, Phone = Phone, Address = Address, City = City, Country = Country, zipCode = zipCode, account_type = account_type, status=status)
            Data.save()
            error = 'User Created Successfully, You can now Login.'
            return redirect("UserLogin")
        except Exception as e:
            newuser.delete()
            error = e

        return TemplateResponse(request,self.template_name,{'error':error})
        

class UserUpdate(TemplateView):
    template_name = "user/user_UpDate.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."


    def get(self,request,UserId):

        context = {'User': UsersAccount.objects.get(Email = UserId)}
        return TemplateResponse(request,self.template_name,context)



    def post(self,request):
        Email = request.POST['Email']
        Password = request.POST['Password']
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        Gender = request.POST['Gender']
        DateOfBirth = request.POST['DateOfBirth']
        Phone = request.POST['Phone']
        Address = request.POST['Address']
        City = request.POST['City']
        Country = request.POST['Country']
        zipCode  = request.POST['zipCode']
        account_type  = request.POST['account_type']
        status = 1
        rec = UsersAccount.objects.filter(Email=request.GET.get(Email))
        rec.update(Email = Email, Password = Password, FirstName = FirstName, LastName = LastName, Gender = Gender, DateOfBirth = DateOfBirth, Phone = Phone, Address = Address, City = City, Country = Country, zipCode = zipCode, account_type = account_type, status=status)
        if account_type == 'Admin':
            return redirect('/user_account/index/')
        else:

            return redirect('/user_account/add_user/')

    
class UserProfile(TemplateView):
    template_name = "user/user_profile.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        if('user_id' in request.session):
            userID = request.session['user_id']
            mainUser = User.objects.get(id=userID);
            user = UsersAccount.objects.get(mainUser=mainUser)

            context = {'user': user}
            return TemplateResponse(request,self.template_name,context)
        else:
            return redirect("siteHome")

class UserOders(TemplateView):
    template_name = "user/user_rating_product.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."
    def get(self,request,UserId):
        context = {'Orders':Orders.objects.filter(customer_id = UserId),'shop_orderlineitems':OrderLineItems.objects.all(),'products': ProductModel.objects.all()}
        return TemplateResponse(request,self.template_name,context)

class User_All_Orders(TemplateView):
    template_name = "user/all_orders_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):

        currentUser = UsersAccount.objects.get(mainUser = request.user)

        AllOrders = Orders.objects.all().filter(orderCustomer = currentUser).order_by('-created_at')


        context = {
            'orders': AllOrders,
            'user': currentUser,
            'totalOrders': 3
        }


        return TemplateResponse(request,self.template_name,context)


class User_Products_Detail(TemplateView):
    template_name = "user/user_products_detial.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,ProductId):
        context = {'Product': ProductModel.objects.get(id = ProductId)}
        return TemplateResponse(request,self.template_name,context)

#######################  admin Section ############################

class AdminDashboard(TemplateView):
    template_name = "admin/admin_dashboard.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."
    

    # UserAccount.objects.get(mainUser = request.user)
    # request.user.email

    def get(self,request):

        allUsers = User.objects.all()
        allOrders = Orders.objects.all()

        lastUsers = allUsers.order_by('-id')[:5]
        lastOrders  = allOrders.order_by('-id')[:5]

        context = {
            'totalUsers': allUsers,
            "totalOrders" : Orders.objects.all(),
            "totalProducts" : ProductModel.objects.all(),
            "lastOrders": lastOrders,
            "lastUsers":lastUsers


        }



        return TemplateResponse(request,self.template_name,context)

class AdminAllOrders(TemplateView):
    template_name = "admin/admin_orders.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):

        context = {'Orders': Orders.objects.all()}
        
        return TemplateResponse(request,self.template_name,context)

    def post(self,request):
#         Confirm an order status to shipped

        try:
            mainOrder = Orders.objects.get(id=request.POST['id'])
            mainOrder.shipping_status = 1
            mainOrder.save()

        except:
            return redirect("AdminAllOrders")

        return redirect("AdminAllOrders")




class ManageOrder(TemplateView):
    template_name = "admin/admin_manage_order.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,OrderId):

        context = {}

        try:
            mainOrder = Orders.objects.get(id=OrderId)

            lineItems = OrderLineItems.objects.all().filter(order_id=mainOrder)

            context = {
                "order" : mainOrder,
                "lineItems":lineItems,
            }
        except:
            context = {}


        return TemplateResponse(request,self.template_name,context)
   
    def post(self,request):
        ids = request.POST['id']
        status = 1
        rec = Orders.objects.filter(id=ids)
        rec.update(shipping_status = status)
        return redirect('/user_account/admin_dashboard/')

class AdminUserSignUp(TemplateView):
    template_name = "admin/admin_add_user.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        return TemplateResponse(request,self.template_name)
   
    def post(self,request):
        Email = request.POST['Email']
        Password = request.POST['Password']
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        Gender = request.POST['Gender']
        DateOfBirth = request.POST['DateOfBirth']
        Phone = request.POST['Phone']
        Address = request.POST['Address']
        City = request.POST['City']
        Country = request.POST['Country']
        zipCode  = request.POST['zipCode']
        account_type  = 'Admin'
        status = 1
        user_exists = User.objects.all().filter(username  = Email)


        if(user_exists):
            return TemplateResponse(request, self.template_name, {'error': 'User with this email already exists.'})

        newuser = User.objects.create_user(Email,Email,Password)
        newuser.first_name = FirstName
        newuser.last_name = LastName
        newuser.save()
        userdetail = User.objects.get(username = Email)
        mainUser =userdetail.id

        Data = UsersAccount(Email=Email,mainUser=mainUser, Gender = Gender, DateOfBirth = DateOfBirth, Phone = Phone, Address = Address, City = City, Country = Country, zipCode = zipCode, account_type = account_type, status=status)
        Data.save()
        return TemplateResponse(request,self.template_name,{'error':'User Register Succefully'})
        


class AdminAllUsers(TemplateView):
     
    template_name = "admin/admin_alluser_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        
        # admin_user_id = request.session['admin_user_id']
        account_type = 'customer'

        data = list()

        allUsers = UsersAccount.objects.filter(account_type= account_type)

        if(allUsers is not None):

            for userInfo in allUsers:


                data.append({
                    "email": userInfo.mainUser.email,
                    "phone":userInfo.Phone,
                    "city": userInfo.City,
                    "address": userInfo.Address,
                    "id":userInfo.mainUser.id,
                    "status":userInfo.status
                })



        context = {"data": data}
        return TemplateResponse(request,self.template_name,context)  


class AdminAllUsersDelete(TemplateView):
    template_name = "admin/admin_all_super_user_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,UserId):
        account_type = 'Client'

        rec = User.objects.filter(id=UserId);
        # rec = User.objects.filter(username= UserId)
        rec.delete()
        rec = UsersAccount.objects.filter(mainUser_id= UserId)
        rec.delete()
        context = {'UsersAccounts': UsersAccount.objects.filter(account_type= account_type), 'User':User.objects.all()}   
        # return TemplateResponse(request,self.template_name,context)   
        return redirect("AdminAllUsers")  

class AdminAllUsersActive(TemplateView):
    template_name = "admin/admin_all_super_user_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,user_id):

        return redirect("siteHome")

    def post(self,request,user_id):

        try:
            if('user_id' in request.session):

                # Validating that the user is admin
                mainUser = User.objects.get(id=request.session['user_id'])
                userObj = UsersAccount.objects.get(mainUser=mainUser)

                if(userObj.account_type == 'admin'):

                    # User to Perform function on.
                    user_id = user_id

                    topUserLevel = User.objects.get(id=user_id)

                    if(topUserLevel is not None):

                        userAccountObj = UsersAccount.objects.get(mainUser=topUserLevel)

                        if(userAccountObj is not None):
                            userAccountObj.status = 1
                            userAccountObj.save()


                            # Redirect back to all users page
                            return redirect("AdminAllUsers")


                else:
                    return redirect("siteHome");
        except:
            return redirect("siteHome");






class AdminAllSuperUsers(TemplateView):
     
    template_name = "admin/admin_all_super_user_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."



    def get(self,request):
        account_type = 'Admin'
        userAccountInfo = UsersAccount.objects.filter(account_type='admin')

        data = list()

        if  userAccountInfo is not None:
            for userInfo in userAccountInfo:

                data.append({
                    "email":userInfo.mainUser.email,
                    "phone":userInfo.Phone,
                    "city":userInfo.City,
                    "id": userInfo.mainUser.id,
                    "address":userInfo.Address,
                    "status":userInfo.status
                })



        context = {"data":data}
        return TemplateResponse(request,self.template_name,context)       

class AdminAllSuperUsersActive(TemplateView):
    template_name = "admin/admin_all_super_user_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,UserId):
        account_type = 'Admin'
        rec = UsersAccount.objects.filter(Email= UserId)
        rec.update( status = '1')
        context = {'UsersAccounts': UsersAccount.objects.filter(account_type= account_type), 'User':User.objects.all()}   
        return TemplateResponse(request,self.template_name,context)     



class AdminAllSuperUsersDelete(TemplateView):
     
    template_name = "admin/admin_all_super_user_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,UserId):
        account_type = 'Admin'
        rec = User.objects.filter(username= UserId)
        rec.delete()
        rec = UsersAccounts.objects.filter(Email= UserId)
        rec.delete()
        context = {'UsersAccounts': UsersAccount.objects.filter(account_type= account_type), 'User':User.objects.all()}   
        return TemplateResponse(request,self.template_name,context)     

class LogoutUser(TemplateView):

    def get(self,request):
        logout(request)
        # Session.objects.all().delete()
        return redirect("siteHome")


class AdminUpDate(TemplateView):
    template_name = "admin/admin_user_update.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,UserId):

        isAdminControl = UsersAccount.objects.get(mainUser=request.user)

        context = {
            'User': UsersAccount.objects.get(mainUser = UserId),
            'mainUser': User.objects.get(id=UserId),
            'isAdminControl':isAdminControl.account_type
            }
        return TemplateResponse(request,self.template_name,context)

    def post(self,request,UserId):

        mainUser = User.objects.get(id=UserId)

        userAccountObject = UsersAccount.objects.get(mainUser = mainUser)

        firstname = request.POST['FirstName']
        lastname = request.POST['LastName']

        city = request.POST['City']
        country = request.POST['Country']

        phone = request.POST['Phone']

        address = request.POST['Address']

        account_type = request.POST['account_type']

        password = request.POST['Password']
        confirmPassword = request.POST['RePassword']




        if(password != ''):
            if(password == confirmPassword):
        #         IF A Password update requested
                    mainUser.set_password(password)

        mainUser.first_name = firstname
        mainUser.last_name = lastname
        mainUser.save()

        userAccountObject.City = city
        userAccountObject.Country = country
        userAccountObject.account_type = account_type
        userAccountObject.Phone = phone
        userAccountObject.Address = address
        userAccountObject.save()

        return redirect(reverse('edit_user',args=[mainUser.id]))



class AdminAddProducts(TemplateView):
    template_name = "admin/admin_add_product.html"

    def get(self,request):


        context = {
            'page_title': 'Add Products'
        }



        return TemplateResponse(request,self.template_name,context)

    def post(self,request):

        prodTitle = request.POST['prod_name']
        prodDesc = request.POST['prod_description']
        prodPrice = request.POST['prod_price']


        uploadedFile = request.FILES['featured_image']

        file_name = default_storage.save(uploadedFile.name, uploadedFile)
        file_url = default_storage.url(file_name)

        ProductModel.objects.create(name=prodTitle,description=prodDesc,price=prodPrice,featured_img_url=file_url,stock=50)

        context = {}

        context["notification"] = {"message": "The Product has been successfully added.",
                                   "type": "success"}
        return TemplateResponse(request, self.template_name,context)





# Edit Product Control


class AdminEditProduct(TemplateView):
    template_name = "admin/admin_edit_product.html"

    def get(self,request,ProdId):

        productToEdit = ProductModel.objects.get(id=ProdId)

        context = {
            'page_title': 'Edit Products',
            'product':productToEdit,
        }



        return TemplateResponse(request,self.template_name,context)

    def post(self,request,ProdId):


        prodToEdit = ProductModel.objects.get(id=ProdId)

        prodTitle = request.POST['prod_name']
        prodDesc = request.POST['prod_description']
        prodPrice = request.POST['prod_price']

        if(request.FILES):
            uploadedFile = request.FILES['featured_image']

            file_name = default_storage.save(uploadedFile.name, uploadedFile)
            file_url = default_storage.url(file_name)
            prodToEdit.featured_img_url = file_url

        prodToEdit.name = prodTitle
        prodToEdit.description = prodDesc
        prodToEdit.price = prodPrice

        prodToEdit.save()

        context = {
            'pageTitle':'Edit Product'
        }

        context["notification"] = {"message": "The Product has been successfully Updated.",
                                   "type": "success"}
        return redirect(to="Admin_All_Products")



class Admin_All_Products(TemplateView):
    template_name = "admin/admin_all_products_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request):
        context = {'Products': ProductModel.objects.all()}
        return TemplateResponse(request,self.template_name,context)



class Admin_Products_Delete(TemplateView):
    template_name = "admin/admin_all_products_view.html"
    page_title = "MorningShop | Your AI Based Grocery Experience."

    def get(self,request,ProductId):
        rec = ProductModel.objects.filter(id= ProductId)
        rec.delete()
        context = {'Products': ProductModel.objects.all()}
        return TemplateResponse(request,self.template_name,context)



      

def restrictUserAccess(user,restrctTo = ''):
    if(getUserType(user) == restrctTo):
        return True
    else:
        if(getUserType(user) == False):
            return redirect("UserLogin")
        elif(getUserType(user) == 'customer'):
            return redirect("userdashboard")
        elif(getUserType(user) == 'admin'):
            return redirect("adminDashboard")

    return True


# Returns string of "user" or "admin" for user typess
def getUserType(user):

    if(user is None):
        return False

    if(UsersAccount.objects.get(mainUser=user).account_type == 'admin'):
        return 'admin'
    elif(UsersAccount.objects.get(mainUser=user).account_type == 'customer'):
        return 'customer'

    return False