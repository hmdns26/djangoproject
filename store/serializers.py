from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255)
    description=serializers.CharField(max_length=500)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    unit_price=serializers.DecimalField(max_digits=6,decimal_places=2)
    inventory=serializers.IntegerField()
    category=CategorySerializer()