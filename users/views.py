from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction

from .serializers import UserSignupSerializer

User = get_user_model()

def get_tokens_for_user(user):
    serializer = UserSignupSerializer(user)
    refresh = RefreshToken.for_user(user)
    return {
        "user": {**serializer.data},
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccessTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    def post( self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({
                "success": False,
                "message": "Refresh Token not Provided",
                "status": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                refresh = RefreshToken(refresh_token)
                return Response({
                    "success":True,
                    "message":"Access Token Generated successfully",
                    "data":{
                        "access_token":str(refresh.access_token)
                    }
                },status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "success":False,
                    "message":str(e),
                },status=status.HTTP_401_UNAUTHORIZED)

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    @transaction.atomic
    def post( self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                "success":True,
                "message":"User Created Successfully",
                "data":{**serializer.data}
                }
                ,status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                "success":False,
                "message":serializer.errors,
                "data":None
            },status=status.HTTP_400_BAD_REQUEST)
        
class FetchUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        user_data = [{
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "mobile": user.mobile,
            "my_field": user.my_field,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "date_joined": user.date_joined,
            "groups": [group.name for group in user.groups.all()],
            "user_permissions": [perm.codename for perm in user.user_permissions.all()]
        } for user in users if user.id != request.user.id]
        if (user_data.__len__() >0):
            return Response({
                "success": True,
                "message": "Users Fetched SuccessFully",
                "data": [*user_data]
            })
        else:
            return Response({
                "success": False,
                "message": "No Users Found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)
    
class SigninView(APIView):
    permission_classes = [permissions.AllowAny]
    @transaction.atomic
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:    
            return Response({
                'success': False,
                'status': 400,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'status': 400,
                'message': 'User Does Not Exist'
            }, status=status.HTTP_404_NOT_FOUND)

        authenticated_user = authenticate(email=email, password=password)
        
        if not authenticated_user:
            return Response({
                'success': False,
                'status': 400,
                'message': 'Wrong Password'
            }, status=status.HTTP_401_UNAUTHORIZED)


        user_data = get_tokens_for_user(authenticated_user)

        return Response({
            'success': True,
            'status': 200,
            'data': user_data
        }, status=status.HTTP_200_OK) 