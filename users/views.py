from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from tokens.models import BlacklistedToken
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from .models import User
from users.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db import IntegrityError
import uuid
import requests


# class CsrfTokenView(APIView):
#     @method_decorator(ensure_csrf_cookie)
#     def get(self, request):
#         csrf_token = get_token(request)
#         return JsonResponse({'csrfToken': csrf_token})
#
#
# def get_csrf_token(session):
#     response = session.get('http://127.0.0.1:8000/get-csrf-token/')
#     return response.json().get('csrfToken')
#
#
# def with_csrf_protection(view_func):
#     def wrapper(self, request, *args, **kwargs):
#         try:
#             response = view_func(self, request, *args, **kwargs)
#             if response.status_code == 403:
#                 # Получаем новый CSRF-токен и повторяем запрос
#                 session = requests.Session()
#                 csrf_token = get_csrf_token(session)
#                 request.META['HTTP_X_CSRFTOKEN'] = csrf_token
#                 response = view_func(self, request, *args, **kwargs)
#             return response
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return wrapper


class RegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 3 or len(password) > 32:
            return Response({"error": "Password length must be between 3 and 32 characters."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        activation_link = str(uuid.uuid4())
        user.activation_link = activation_link
        user.save()

        activation_url = f"http://localhost:8000/activate/{activation_link}/"
        send_mail(
            'Activate your account',
            f'Click the link to activate your account: {activation_url}',
            'sashabolokan2016@mail.ru',
            [email],
        )

        return Response({"message": "User registered successfully."
                                    " Please check your email to activate your account."}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    def get(self, request, link):
        user = get_object_or_404(User, activation_link=link)

        if user.is_active:
            return Response({"message": "Account already activated."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.activation_link = None
        user.save()

        return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie(
            key='jwt',
            value=str(refresh.access_token),
            httponly=True
        )
        response.data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Вы успешно вышли из системы'
        }
        return response


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().values('id', 'email', 'is_active')
        return Response(users)


class MainView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
