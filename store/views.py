from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product ,Comment
from .serializers import CategorySerializer, CommentSerializer, ProductSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class ProductViewSet(ModelViewSet):
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category_id']
    queryset=Product.objects.all()
    
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

class CommentViewSet(ModelViewSet):
    serializer_class=CommentSerializer 
    def get_queryset(self):
        product_pk=self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()                                       
    def get_serializer_context(self):
        return {"product_pk":self.kwargs['product_pk']}