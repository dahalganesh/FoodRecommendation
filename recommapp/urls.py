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
    path( "my-cart/", MyCartView.as_view(), name = 'mycart'),


]

 