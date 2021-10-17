from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, ShippingAddress, Review


class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        # 2 required attributes. model and fields
        model=User
        # we dont want password back
        fields=['id', 'username', 'email','name', 'isAdmin']
    # we add a name field. we could do this through migrations again but it takes alotof work
    def get_name(self,obj):
        name=obj.first_name
        if name =='':
            name=obj.email
        return name
    # instead of is_staff, I want to change it to isAdmin
    def get_isAdmin(self,obj):
        return obj.is_staff

# we use this when user first registers or sets its account
class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id', 'username', 'email', 'name', 'isAdmin', 'token']
    def get_token(self,obj):
        # we take the user obj and we return back another token with the initial response
        token=RefreshToken.for_user(obj)
        return str(token.access_token)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'

# this will wrap up our model and turn it to json format
class ProductSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    class Meta:
        # 2 required attributes. model and fields
        model=Product
        fields='__all__'
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer=ReviewSerializer(reviews, many=True)
        return serializer.data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        # 2 required attributes. model and fields
        model=ShippingAddress
        fields='__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # 2 required attributes. model and fields
        model=OrderItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    # handling nested object serializing
    orderItems=serializers.SerializerMethodField(read_only=True)
    shippingAddress=serializers.SerializerMethodField(read_only=True)
    user=serializers.SerializerMethodField(read_only=True)
    class Meta:
        # 2 required attributes. model and fields
        model=Order
        fields='__all__'
    def get_orderItems(self,obj):
        items=obj.orderitem_set.all()
        serializer=OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self,obj):
        try:
            #this one-toone field. thats why we can access it like this
            address=ShippingAddressSerializer(obj.shippingaddress,many=False).data
        except:
            address=False      
        return address

    def get_user(self,obj):
        user=obj.user
        serializer=UserSerializer(user, many=False)
        return serializer.data