import datetime

import jwt
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User

from .serializers import UserSerializer


# from .utils import decode_activation_token, generate_activation_token


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # token = generate_activation_token(user.id)
        #
        # frontend_base_url = FRONTEND_BASE_URL
        # subject = 'Welcome to Our Service'
        # message = (
        #     f"Thank you for registering. Your account is currently inactive. "
        #     f"For activate click this link: {frontend_base_url}/activate/{token}/")  # {activation_link}
        # # f"For activate click this link: http://localhost:8000/api/activate/{user.id}/")
        # from_email = 'digitalautoservice2024@gmail.com'
        # recipient_list = [user.email]
        #
        # send_mail(subject, message, from_email, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed('User not found or password is incorrect')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return Response({'jwt': token, 'id': user.id})
