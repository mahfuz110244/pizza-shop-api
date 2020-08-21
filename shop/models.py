from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from core.models import BaseModel
from user.models import Customer


# Create your models here.
class Tags(BaseModel):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '02. Tags'
        ordering = ['name']


class Pizza(BaseModel):
    YES = 'yes'
    NO = 'no'
    AVAILABILITY_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]
    name = models.CharField(max_length=256, unique=True)
    brand = models.CharField(max_length=256)
    availability = models.CharField(
        max_length=9,
        choices=AVAILABILITY_CHOICES,
        default=YES,
    )
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    weight = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    image = models.FileField(upload_to='uploads/pizza/', default="/pizza.png", blank=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # app_label = 'shop'
        verbose_name_plural = '03. Pizzas'
        ordering = ['name']


class Order(BaseModel):
    SUBMITTED = 'submitted'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    DELIVERED = 'delivered'
    ORDER_STATE_CHOICES = [
        (SUBMITTED, 'Submitted'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (DELIVERED, 'Delivered')
    ]
    pizza = models.ForeignKey(Pizza, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    order_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    address = models.TextField(max_length=500)
    latitude = models.FloatField(max_length=50, blank=True, default=0)
    longitude = models.FloatField(max_length=50, blank=True, default=0)
    order_state = models.CharField(
        max_length=9,
        choices=ORDER_STATE_CHOICES,
        default=SUBMITTED,
    )
    delivery_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.pizza}"

    class Meta:
        # app_label = 'shop'
        verbose_name_plural = '04. Orders'
        # ordering = ['id']
