from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=request.data.get('username'))
        token = Token.objects.get(user=user)

        serializer = UserSerializer(user)

        data = {
            "user":serializer.data,
            "token":token.key
        }        

        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    data = request.data
    authenticated_user = authenticate(username=data['username'], password=data['password'])

    if authenticated_user is not None:
        user = User.objects.get(username=data['username'])
        serializer = UserSerializer(user)

        response_data = {
            "user":serializer.data
        }

        token,created_token = Token.objects.get_or_create(user=user)

        if token:
            response_data['token']=token.key
        elif created_token:
            response_data['token']=created_token.key

        return Response(response_data, status=status.HTTP_200_OK)
    return Response({"detail":"not found"}, status=status.HTTP_404_NOT_FOUND)