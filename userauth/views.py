from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import UserRegistrationSerializer
from rest_framework_jwt.settings import api_settings
import datetime
from django.utils import timezone


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.user.is_anonymous)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return Response({'details': 'please logout to continue'}, status=HTTP_400_BAD_REQUEST)
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username))
        if qs.exists():
            user_obj = qs.first()
            user = authenticate(username=user_obj.username, password=password)
            if user:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = Response(
                    {
                        'token': token,
                        'user': user.username
                    },
                    content_type="application/json",
                    status=HTTP_200_OK)
                expiration = (timezone.now() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
                return response
        return Response(
            {'error': 'Invalid Credentials'},
            content_type="application/json",
            status=HTTP_401_UNAUTHORIZED
        )


class RegisterUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class Logout(APIView):

    def get(self, request, *args, **kwargs):
        response = Response(
            {'details': 'successfully logout'}, status=HTTP_200_OK)
        response.delete_cookie('JWT')
        return response
