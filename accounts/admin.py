from django.contrib import admin
from .models import Customer, Products, Order,Tag
# Register your models here.

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Tag)
admin.site.register(Order)
