from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255)
    description=serializers.CharField(max_length=500)

class ProductSerializer(serializers.ModelSerializer):

    category=serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name='categorydetails')
    class Meta:
        model=Product
        fields=['id','name','unit_price','category','unit_price','inventory','slug','description']
