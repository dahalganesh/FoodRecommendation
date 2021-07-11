from django.contrib.auth import authenticate, login, logout
from django.forms.widgets import PasswordInput
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls.conf import path
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm


from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import *   
from .forms import RegisterPageForm, LoginPageForm


def items(request):
    categorys = Category.objects.all().order_by("-id")
    context = {'categorys':categorys}
    return render(request,'items.html',context)

class IndexView(TemplateView):
    template_name = "index.html"



class RegisterView(CreateView):
    template_name ='register.html'
    form_class = RegisterPageForm
    success_url= reverse_lazy("recommapp:items")  

    def form_valid(self, form):
        username= form.cleaned_data.get('username')
        Password = form.cleaned_data.get('password')
        full_name = form.cleaned_data.get('full_name')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        address = form.cleaned_data.get("address")
        phone =  form.cleaned_data.get('phone')
        email= form.cleaned_data.get('email')
        user = User.objects.create_user(username,email,Password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)  


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("recommapp:items")


       


class LoginView(FormView):
    template_name ='login.html'
    form_class = LoginPageForm
    success_url= reverse_lazy("recommapp:items")  

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        p = form.cleaned_data.get('password')
        usr = authenticate(username = uname, password= p)
        if usr is not None and usr.customer:
            login(self.request, usr)
        
        else:
            return render(self.request, self.template_name,{'form':self.form_class, 'error':'Invalid Username'})

        return super().form_valid(form)






class AddToCartView(TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # get product ID from request URL.
        product_id = self.kwargs['pro_id']
     
        # get product.
        product_obj = Product.objects.get(id = product_id)

        #check if cart exists.  
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product= product_obj)
            # items alreay exist in the cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity+= 1
                cartproduct.subtotal+= product_obj.price
                cartproduct.save()
                cart_obj.total+= product_obj.price
                cart_obj.save()
            # new items is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart = cart_obj,
                    product = product_obj,
                    rate = product_obj.price,
                    quantity = 1,
                    subtotal = product_obj.price,
                )
                cart_obj.total+= product_obj.price
                cart_obj.save()


        else:
            cart_obj = Cart.objects.create(total = 0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                    cart = cart_obj,
                    product = product_obj,
                    rate = product_obj.price,
                    quantity = 1,
                    subtotal = product_obj.price
                )
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context
    



class MyCartView(TemplateView):
    template_name ='mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id= cart_id)
        else:
            cart = None
        context['cart']= cart

        return context









 
