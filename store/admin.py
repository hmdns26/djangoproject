from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','created_at']