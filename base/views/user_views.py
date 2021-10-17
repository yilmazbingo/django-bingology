from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from rest_framework.response import Response
# now we have to use base to import from base
from base.serializers import ProductSerializer,UserSerializer,UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data =super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        print("serializer in token",serializer)
        for k,v in serializer.items():
            # print("data[k",data[k])
            data[k]=v
        return data
# we are overriding TokenObtainPairView's serializer method
# this will be used in urls
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data=request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

            # when we register a user, we want to return token right away
        serializer=UserSerializerWithToken(user, many=False)
            # dont login the user
        return Response(serializer.data)
    except:
        message={'detail':"User with this email already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    # Because we use @api_view, this user, will be the user from the token. deocrator expects to see a token
    user=request.user
    print('user',user)
    # when we update the user, we need a new token
    serializer = UserSerializerWithToken(user, many=False)
    data=request.data
    user.first_name=data['name']
    # I save the username as email
    user.username=data['email']
    user.email=data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # Because we use @api_view, this user, will be the user from the token. deocrator expects to see a token
    user=request.user
    # this data has to be serialized before turned back to front end. it worked fine with django, but now we use drf
    # we need to create serializer for every different model
    # many is for serializing multiple object. we are getting single object
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    print(request)
    users=User.objects.all()
    serializer=UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request,pk):
    userForDeletion=User.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    user=User.objects.get(id=pk)
    serializer=UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
    print("pk",pk)
    user = User.objects.get(id=pk)
    print("user",user)

    data=request.data
    print("data",data)
    user.first_name=data['name']
    user.username=data['email']
    user.email=data['email']
    user.is_staff=data['isAdmin']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
