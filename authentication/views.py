import json
from django.views.decorators.csrf import csrf_exempt
# from models import User_collection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
# from .models import EmailToken
import secrets
from authentication.jwt_utils import generate_jwt_token, get_token_from_request, decode_jwt_token
from authentication.models import User_collection


# Create your views here.

def generate_token(email):
    # Generate a unique token
    token = secrets.token_urlsafe(32).join(email)

    # Save the token to the database
    return token


def is_user(user):
    return user.get('role') == 'User'


@csrf_exempt
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        # confirmedPassword = data.get('confirmedPassword')
        # if password != confirmedPassword:
        #     return Response({"message": "password not the same"}, status=status.HTTP_400_BAD_REQUEST)

        check = User_collection.find_one({"email": email})
        if check is None:
            new_user = {
                    'name': name,
                    'email': email,
                    'password': password,
                    'role': 'User'
            }
            User_collection.insert_one(new_user)
            return Response({"message": "Signup Successfully",
                                 "data": {
                                     'name': name,
                                     'email': email,
                                     'role': 'User'
                                 }}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "email already exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    global user
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        user = User_collection.find_one({"email": email})
        if user:
            if user.get('password') == password:
                token = generate_jwt_token(user)
                return JsonResponse({'token': token})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_user(request):
    token = get_token_from_request(request)
    print(token)
    id_user = decode_jwt_token(token)
    print(id_user)
    return id_user
