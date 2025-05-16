from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import UserSerializer, UserSerializerWithToken
from base.models import Product
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
       data = super().validate(attrs)
       serializer = UserSerializerWithToken(self.user).data
       for key, value in serializer.items():
           data[key] = value

       return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfileDetails(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfileDetails(request):
    user = request.user
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    password = data.get('password', None)
    if password and password != '':
        user.password = make_password(data['password'])
    user.save()
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create(
            first_name = data['first_name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = 'User with this email already exists'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(pk = pk)
    userForDeletion.delete()
    return Response("User Deleted Successfully :D")


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    user.is_staff = data.get('isAdmin', user.is_staff)
    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)