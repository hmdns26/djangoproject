from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    num_of_products=serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields=['id','title','description','num_of_products']
    def get_num_of_products(self,category):
        return category.products.count()

class ProductSerializer(serializers.ModelSerializer):

    # category=serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name='categorydetails')
    class Meta:
        model=Product
        fields=['id','name','unit_price','category','unit_price','inventory','slug','description']
