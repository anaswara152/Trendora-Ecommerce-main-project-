from django.db import models
from django.contrib.auth.models import User
from manager.models import product

# Create your models here.
class reg(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    city=models.CharField(max_length=18)
    postalcode=models.CharField(max_length=4)
    state=models.CharField(max_length=18)

class cart(models.Model):
    customerid=models.ForeignKey(User,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    count=models.IntegerField()
    price=models.IntegerField()

class whislist(models.Model):
    customerid=models.ForeignKey(User,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)

class ordertb(models.Model):
    name=models.CharField(max_length=20)
    phone=models.CharField(max_length=10,blank=True,null=True) 
    address=models.TextField() 
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    zipcode=models.IntegerField(blank=True,null=True)
    email=models.EmailField()
    orderdate=models.CharField(max_length=20)
    carrier=models.CharField(max_length=20,blank=True,null=True)
    tracking=models.CharField(max_length=20,blank=True,null=True)
    shippingdate=models.CharField(max_length=18,blank=True,null=True)
    transactionid=models.CharField(max_length=20,blank=True,null=True)
    paymentdate=models.CharField(max_length=18,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,default="pending")
    orderstatus=models.CharField(max_length=18,default="pending")
    ordertotal=models.IntegerField()
    customerid=models.ForeignKey(User,on_delete=models.CASCADE)
 

class orderitems(models.Model):
    order=models.ForeignKey(ordertb,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    total=models.IntegerField()
    count=models.IntegerField()
