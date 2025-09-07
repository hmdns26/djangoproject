from djoser.serializers import UserCreateSerializer ,UserSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields=['id','username','password','email','first_name','last_name']

class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields=['id','username','email','first_name','last_name']
