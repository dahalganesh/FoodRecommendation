from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy




class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null= True,blank= True)
    full_name = models.CharField( max_length=50)
    image = models.ImageField(upload_to ="admins")
    mobile = models.CharField( max_length=10)

    def __str__(self):
        return self.user.username



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null= True,blank= True)
    first_name = models.CharField( max_length=200,null = True)
    last_name = models.CharField(max_length=200 , null= True)
    full_name = models.CharField(max_length=200 , null= True)
    address = models.CharField ( max_length= 200 , null= True)
    phone = models.CharField(max_length=10)
    
    

    def __str__(self):
        return self.full_name if self.full_name else str(self.id)




    



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

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Esewa", "Esewa"),
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
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    date_added = models.DateTimeField(auto_now_add= True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)


    def __str__(self):
        return "order:"+str(self.id)




class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL,blank= True,null= True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null= True, blank=True)
    comment = models.CharField(max_length= 200)
    rate = models.IntegerField(default= 0)
    created_at = models.DateTimeField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)
    

    



    

 

    

