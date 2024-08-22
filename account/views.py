from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.core.mail import send_mail

# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password'])
            )
            return Response("Your Account has been Created Successfully!", status=status.HTTP_201_CREATED)
        else:
            return Response("Email already exists!", status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def authUser(request):
    user = UserSerializer(request.user, many=False  )
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email'] 

    if data['password'] != "" :
        user.password = make_password(data['password'])

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email = data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = "{host}api/reset-password/{token}".format(host=host ,token=token)

    body = "Your Password Reset Link is : {link}".format(link=link)
    send_mail(
        "password Reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response("Password Reset Link Sent to {email}".format(email=data['email']))



@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response("Token Expired", status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response('Passwords are not Equal', status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response('Password Reset Done :)')