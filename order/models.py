from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from product.models import Product


class ShopCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()

    def __str__(self):
        return self.product

    @property
    def amount(self):
        return round((self.quantity * self.product.price),2)

    @property
    def price(self):
        return self.product.price

class ShopCartForm(ModelForm):
    class Meta:
        model=ShopCart
        fields=['quantity']

class Order(models.Model):
    Status=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Preparing','Preparing'),
        ('OnShipping','OnShipping'),
        ('Completed','Completed'),
        ('Canceled','Canceled'),
    )

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code=models.CharField(max_length=5,editable=False)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    phone=models.CharField(blank=True,max_length=20)
    tableno=models.CharField(blank=True,max_length=10)
    address=models.CharField(blank=True,max_length=150)
    city=models.CharField(blank=True,max_length=25)
    country=models.CharField(blank=True,max_length=20)
    total=models.FloatField()
    deliverytime=models.CharField(max_length=35,default='As fast as possible')
    status=models.CharField(max_length=10,choices=Status,default='New')
    ip=models.CharField(max_length=20,blank=True)
    adminnote=models.CharField(blank=True,max_length=150)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields = ['first_name','last_name','phone','tableno','deliverytime']


class OrderProduct(models.Model):
    Status=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled')
    )

    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.FloatField()
    amount=models.FloatField()
    status=models.CharField(max_length=10,choices=Status,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

