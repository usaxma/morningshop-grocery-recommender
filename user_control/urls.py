from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required




urlpatterns = [
    # admin section 
    path('admin_dashboard/',AdminDashboard.as_view(),name="admin_dashboard"),
    path('all_orders/',AdminAllOrders.as_view(),name="AdminAllOrders"),
    path('manage_order/<int:OrderId>',ManageOrder.as_view(),name="manage_order"),
    path('manage_order/',ManageOrder.as_view(),name="manage_order"),
    # # User Manage section 
    path('add_user/',AdminUserSignUp.as_view(),name="add_user"),
    path('all_users/',AdminAllUsers.as_view(),name="AdminAllUsers"),
    path('all_super_users/',AdminAllSuperUsers.as_view(),name="AdminAllSuperUsers"),
    path('edit_user/<int:UserId>',AdminUpDate.as_view(),name="edit_user"),
   
    path('delete_user/<int:UserId>',AdminAllUsersDelete.as_view(),name="AdminAllUsersDelete"),
    path('active_user/<int:user_id>',AdminAllUsersActive.as_view(),name="AdminAllUsersActive"),

    # Depriciated, using only one for all user types
    path('active_super_user/<int:UserId>',AdminAllSuperUsersActive.as_view(),name="AdminAllSuperUsersActive"),
    path('delete_super_user/<int:UserId>',AdminAllSuperUsersDelete.as_view(),name="AdminAllSuperUsersDelete"),
    
    # # User Manage section 
    path('admin_dashboard/',AdminDashboard.as_view(),name="admin_dashboard"),

    path('add_product/', AdminAddProducts.as_view(), name="add_product"),
    path('admin_all_products/',Admin_All_Products.as_view(),name="Admin_All_Products"),
    path('admin_products_delete/<int:ProductId>',Admin_Products_Delete.as_view(),name="Admin_Products_Delete"),
    path('edit_product/<int:ProdId>',AdminEditProduct.as_view(),name="edit_product"),
    
    path('user_orders/',User_All_Orders.as_view(),name="user_orders"),
    path('user_products_detial/<int:ProductId>',User_Products_Detail.as_view(),name="User_Products_Detail"),
    
    # user section
    path('home/',UserHome.as_view(),name="index"),
    path('orders/<int:UserId>',UserOders.as_view(),name="oders"),
    path('login/',UserLogin.as_view(),name="UserLogin"),
    path('sign_up/',UserSignUp.as_view(),name="UserSignUp"),
    path('user_update/',AdminUpDate.as_view(),name="user_update"),
    path('user_update/<str:UserId>',AdminUpDate.as_view(),name="user_update"),
    path('profile/',UserProfile.as_view(),name="profile"),
    path('logout/',LogoutUser.as_view(),name="logout"),

]