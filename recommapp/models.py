from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null= True,blank= True)
    first_name = models.CharField( max_length=200,null = True)
    last_name = models.CharField(max_length=200 , null= True)
    full_name = models.CharField(max_length=200 , null= True)
    address = models.CharField ( max_length= 200 , null= True)
    phone = models.CharField(max_length=10)
    

    def __str__(self):
        return self.full_name



class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.title
    

class Product(models.Model):
    title = models.CharField( max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to ='products')
    Category = models.ForeignKey(Category, on_delete = models.CASCADE)
    description = models.TextField()
    price = models.FloatField() 


    def __str__(self):
        return self.title




class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL,blank= True,null= True)
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
         return "Cart:" + str(self.id)
     


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

   


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing","Order Processing"),
    ("On the way", "On the way"),
    ("Order Complete","Order Complete"),
    ("Order Canceled","Order Canceled"),
)




class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    Order_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    mobile  = models.CharField(max_length=10)
    email = models.EmailField(null= True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50 , choices=ORDER_STATUS)
    date_added = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return "order:"+str(self.id)
    



    

 

    

