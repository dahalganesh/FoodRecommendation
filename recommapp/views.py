from django import urls
from django.contrib.auth import authenticate, login, logout
from django.db.models.aggregates import Avg, Count, Sum
from django.forms.widgets import PasswordInput
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.urls.conf import path
from django.views.generic import View, TemplateView, CreateView,DetailView,ListView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings




from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
import requests

from .models import *   
from .forms import  RegisterPageForm, LoginPageForm, CheckOutForm,ReviewForm
from recommapp import forms
from django.db.models import Q







class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id= cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()            
        return super().dispatch(request, *args, **kwargs)




def items(request):
    categorys = Category.objects.all().order_by("-id")
    reviews = Review.objects.values("product").annotate(avgrate=Avg('rate'))
    
    for c in categorys:
        for p in c.product_set.all():
            for r in  Review.objects.values("product").annotate(avgrate=Avg('rate')):
                context = {'categorys':categorys,'reviews':reviews}
                     # if p.id == r['product']:
                #     p.rate = r['rate']
            #    print('a')
    
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

    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


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
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        
        else:
            return render(self.request, self.template_name,{'form':self.form_class, 'error':'Invalid Username'})

        return super().form_valid(form)
    

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url
     



class AddToCartView(EcomMixin, TemplateView):
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
    



class MyCartView(EcomMixin, TemplateView):
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



class ReviewView(EcomMixin, CreateView):
    template_name ='review.html'
    form_class = ReviewForm
    success_url = reverse_lazy("recommapp:items")

    def dispatch(self, request, *args, **kwargs) :
        product_id = self.kwargs["pro_id"]
        if request.user.is_authenticated and Customer.objects.filter(user= request.user).exists():
            pass
        else:
            return redirect("/login/?next=/review/", kwargs={'pro_id':product_id})

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs["pro_id"]
        product = Product.objects.get(id= product_id)
        context['products'] = product
        return context
  
    def form_valid(self, form):
        # user_id = self.request.session.get("user_id")
        user_id = self.request.user.id
        # print(self.request.user.is_authenticated)
        product_id = self.kwargs["pro_id"]
       
        if self.request.user.is_authenticated:
            product = Product.objects.get(id= product_id)
            customer = Customer.objects.get(id=user_id)
            form.instance.customer = customer
            form.instance.product = product
            review = form.save()
        
        else:
            return redirect("recommapp:items")

        return super().form_valid(form)

   
    
   



class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("recommapp:items")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Esewa":
                return redirect(reverse("recommapp:esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("recommapp:items")
        return super().form_valid(form)


class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        order_obj = Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.payment_completed = True
            order_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)
            


class CartManage(EcomMixin, View):
    def get(self,request,*args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('Action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj =cp_obj.cart

        if action =="inc":
            cp_obj.quantity +=1
            cp_obj.subtotal +=cp_obj.rate   
            cp_obj.save()
            cart_obj.total +=cp_obj.rate
            cart_obj.save()

        elif action=="dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity== 0:
                cp_obj.delete()


        elif action =="rmv":
                cart_obj.total -= cp_obj.subtotal
                cart_obj.save()
                cp_obj.delete()

    
        return  redirect("recommapp:mycart")

class DeleteCart(EcomMixin, View):
    def get(self ,request,*args, **kwargs):
        cart_id =request.session.get('cart_id',None)
        if cart_id:
            cart= Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart .save()
        return redirect('recommapp:mycart')


class SearchView(EcomMixin, TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        result = Product.objects.filter(Q(title__contains= kw)| Q(description__contains=kw))
        context['results'] = result
        return  context




class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and Customer.objects.filter(user= request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders
        return context



class CustomerOrderDetailsView(DetailView):
    template_name = "orderdetails.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id= order_id)
            if request.user.customer != order.cart.customer:
                return redirect("recommapp:profile" )
        else:
            return redirect("/login/?next=/profile/")
       
        return super().dispatch(request, *args, **kwargs)



#admin site 

class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = LoginPageForm
    success_url = reverse_lazy("recommapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomePageView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context



class AdminOrderDetailsView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetails.html"
    model = Order
    context_object_name = 'ord_obj'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allstatus'] = ORDER_STATUS
        return context



class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name  ="adminpages/adminorderlist.html "
    queryset = Order.objects.all().order_by('-id')
    context_object_name = "allorders"



class AdminOrderStatusChangeView(AdminRequiredMixin, View):  
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id = order_id)
        new_status= request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('recommapp:adminorderdetails', kwargs={'pk':order_id}))
    
