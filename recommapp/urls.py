from django.urls import path
from .views import *
from . import views


app_name= 'recommapp'
urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("register/", RegisterView.as_view(), name='register'),
    path('items/', views.items, name = 'items'),
    path("login/", LoginView.as_view(), name = 'login'),
    path("logout/", LogoutView.as_view(), name = 'logout'),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name ='addtocart'),
    path("my-cart/", MyCartView.as_view(), name = 'mycart'),
    path('cart-manage/<int:cp_id>/', CartManage.as_view(),name= 'cartmanage'),
    path('cart-delete/', DeleteCart.as_view(), name ='cartdelete'),
    path('checkout/', CheckoutView.as_view(), name ='checkout'),
    path('search/', SearchView.as_view(), name='search'),

    path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),
    path("esewa-verify/", EsewaVerifyView.as_view(), name="esewaverify"),

    path("profile/" ,  CustomerProfileView.as_view(), name ='profile'),
    path("profile/order-<int:pk>/", CustomerOrderDetailsView.as_view(), name='orderdetails'),
    path("review/<int:pro_id>/", ReviewView.as_view(), name='review'),
    
    path("admin-login/", AdminLoginView.as_view(), name ='adminlogin'),
    path('admin-home/', AdminHomePageView.as_view(), name ='adminhome'),
    path('admin-order/<int:pk>/', AdminOrderDetailsView.as_view(), name = "adminorderdetails"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name ='adminorderlist' ),
    path("admin-order-<int:pk>-change/",AdminOrderStatusChangeView.as_view(), name = 'adminorderstatuschange'),
    

  
]

 