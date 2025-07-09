from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

class ProductList(APIView):
    def get(self,request):
        product_queryset=Product.objects.select_related('category').all()
        serializer=ProductSerializer(product_queryset,many=True,context={
            'request':request
        })
        return Response(serializer.data)
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class ProductDetails(APIView):
    def get(self , request,pk):
        product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
        serializer=ProductSerializer(product,context={'request':request})
        return Response(serializer.data)
    def put(self ,request,pk):
        product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)  
    def delete(self , request,pk):
        product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
        if product.order_items.count()>0:
            return Response({'ereor':'there is some order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    def get(self,request):
        category_queryset=Category.objects.prefetch_related('products').all()
        serializer=CategorySerializer(category_queryset,many=True)
        return Response(serializer.data)
    def put(self,request):
        serializer=CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)   

class CategoryDetalil(APIView):
    def get(self,request,pk):
        category=get_object_or_404(Category,pk=pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data)
    def put(self , request,pk):
        category=get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(category,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self , request,pk):
        category=get_object_or_404(Category,pk=pk)
        if category.products.count()>0:
            return Response({'error':'there is some products relating this category'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    