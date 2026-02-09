from django.db import models

# Create your models here.

#collections here

#Promotions Class
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
#Product Class

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    
#Customer class
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMEBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMEBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]

#ORDER CLASS
class Order(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
#OrderItem Class
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city =  models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField()
    customer =  models.ForeignKey(
        Customer, on_delete=models.CASCADE)

# Chart Class
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

#CartItem Class 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()