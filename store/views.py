from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@api_view(['GET','POST'])
def products_list(request):
    if request.method == 'GET':
        product_queryset=Product.objects.select_related('category').all()
        serializer=ProductSerializer(product_queryset,many=True,context={
            'request':request
        })
        return Response(serializer.data)
    elif request.method =='POST':
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','DELETE'])
def products_details(request,pk):
    product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
    if request.method == 'GET':
        serializer=ProductSerializer(product,context={
            'request':request
        })
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.order_items.count()>0:
            return Response({'ereor':'there is some order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
def category_list(request):
    if request.method == 'GET':
        category_queryset=Category.objects.prefetch_related('products').all()
        serializer=CategorySerializer(category_queryset,many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        serializer=CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)   
    
@api_view(['GET','PUT','DELETE'])
def category_details(request,pk):
    category=get_object_or_404(Category,pk=pk)
    if request.method == 'GET':
        serializer=CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if category.products.count()>0:
            return Response({'error':'there is some products relating this category'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    