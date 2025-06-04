from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.products_list),
    path('products/<int:pk>/',views.products_details),
    path('category/<int:pk>/',views.category_details,name='categorydetails'),
]
