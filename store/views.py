from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.select_related('category').all()   
    def get_serializer_context(self):
        return {
            'request':self.request
        }

    def destroy(self , request,pk):
        product=get_object_or_404(Product.objects.select_related('category'),pk=pk)  
        if product.order_items.count()>0:
            return Response({'ereor':'there is some order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.prefetch_related('products')
    def delete(self , request,pk):
        category=get_object_or_404(Category,pk=pk)
        if category.products.count()>0:
            return Response({'error':'there is some products relating this category'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

                                            
