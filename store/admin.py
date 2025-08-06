from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name",'inventory']

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','created_at']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["title"]