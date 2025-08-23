from rest_framework import serializers
from .models import Cart, CartItem, Category, Product ,Comment

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','name','body']
    def create(self, validated_data):
        product_id=self.context['product_pk']
        return Comment.objects.create(product_id=product_id,**validated_data)
    
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','unite_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product',"quantity"]
    def create(self, validated_data):
        cart_id=self.context['cart_pk']
        product=validated_data.get('product')
        quantity=validated_data.get('quantity')
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product.id)
            cart_item.quantity+=quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(cart_id=cart_id,**validated_data)
        self.instance=cart_item    
        return cart_item
        
class CartItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer()
    item_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
    fields=['id','product','quantity','item_total']

    def get_item_total(self,cart_item):
        return cart_item.quantity * cart_item.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    items =CartItemSerializer(many= True,read_only=True)
    total_price=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=['id','items','total_price']
        read_only_fields=['id',]

    def get_total_price(self,cart):
        return sum([item.quantity *item.product.unit_price for item in cart.items.all()])

class ChangeCartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']