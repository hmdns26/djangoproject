from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@api_view()
def products_list(request):
    product_queryset=Product.objects.select_related('category').all()
    serializer=ProductSerializer(product_queryset,many=True,context={
        'request':request
    })
    return Response(serializer.data)

@api_view()
def products_details(request,pk):
    product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
    serializer=ProductSerializer(product,context={
        'request':request
    })
    return Response(serializer.data)

@api_view()
def category_details(request,pk):
    category=get_object_or_404(Category,pk=pk)
    serializer=CategorySerializer(category)
    return Response(serializer.data)