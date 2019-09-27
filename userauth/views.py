from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from .forms import CustomUserCreationForm
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


class Login(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'details': 'please logout to continue'})
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username))
        if qs.exists():
            user_obj = qs.first()
            user = authenticate(username=user_obj.username, password=password)
            if user:
                auth_login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {'token': token.key},
                    content_type="application/json",
                    status=HTTP_200_OK)

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        auth_logout(request)
        return Response({'details': 'successfully logout'}, status=HTTP_200_OK)
