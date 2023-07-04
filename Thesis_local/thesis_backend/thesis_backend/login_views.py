from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import User
from django.db import connection
from django.core.management import call_command

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    table_name = User._meta.db_table
    if table_name in connection.introspection.table_names():
        print(f"Table '{table_name}' already exists.")
    else:
        print(f"Table '{table_name}' does not exist. Creating...")
        call_command('makemigrations', 'thesis_backend')
        call_command('migrate')
        print(f"Table '{table_name}' created successfully.")

    user_exists = User.objects.filter(Username=username).exists()
    if user_exists:
        return Response({'message':'User already exists'}, status= 400)
    else:
        new_user = User(Username = username, Password = password, Email = email)
        new_user.save()

    # Print the table content
    table_data = User.objects.all()
    print(f"\n{table_name} table content:")
    for user in table_data:
        print(user)

    return Response({'message':'Registration successful'}, status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # user = authenticate(request, username=username, password=password)
    
    if username is not None:
        return Response({'message': 'Login successful'}, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)