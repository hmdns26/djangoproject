from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from store.models import Product
from store.serializers import ProductSerializer

@api_view()
def products_list(request):
    product_queryset=Product.objects.select_related('category').all()
    serializer=ProductSerializer(product_queryset,many=True)
    return Response(serializer.data)

@api_view()
def products_details(request,id):
    product=get_object_or_404(Product.objects.select_related('category'),pk=id)  
    serializer=ProductSerializer(product)
    return Response(serializer.data)