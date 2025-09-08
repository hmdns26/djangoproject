from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Category, Customer, Product ,Comment
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CategorySerializer, ChangeCartitemSerializer, CommentSerializer, CustomerSerializer, ProductSerializer
from rest_framework.viewsets import ModelViewSet ,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin ,DestroyModelMixin
from rest_framework.permissions import IsAdminUser ,IsAuthenticated
from .permissions import IsAdminOrReadOnly
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
    permission_classes=[IsAdminOrReadOnly]
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

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_queryset(self):
        cart_pk=self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return ChangeCartitemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_pk':self.kwargs['cart_pk']}
    
class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    serializer_class=CartSerializer
    queryset=Cart.objects.prefetch_related('items__product').all()
    lookup_value_regex='[0-9a-f]{32}'

class CustomerViewSet(ModelViewSet):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()
    permission_classes=[IsAdminUser]
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id=request.user.id
        customer=Customer.objects.get(user_id=user_id)
        if request.mathod =='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)