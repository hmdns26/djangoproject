from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.products_list),
    path('products/<int:pk>/',views.products_details),
    path('category/',views.category_list),
    path('category/<int:pk>/',views.category_details,name='categorydetails'),
]
