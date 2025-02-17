from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import WasteBot, SmartBin, Waste, User
from .serializers import WasteBotSerializer, SmartBinSerializer, WasteSerializer, UserSerializer
from .decorators import role_required
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use the check_password method to verify the password
    if check_password(password, user.password):
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#User views
@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# WasteBot views
@api_view(['GET', 'POST'])
def wastebot_list(request):
    if request.method == 'GET':
        wastebots = WasteBot.objects.all()
        serializer = WasteBotSerializer(wastebots, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WasteBotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def wastebot_detail(request, pk):
    wastebot = get_object_or_404(WasteBot, pk=pk)

    if request.method == 'GET':
        serializer = WasteBotSerializer(wastebot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WasteBotSerializer(wastebot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = WasteBotSerializer(wastebot, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Verify that the user is an admin
        wastebot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# SmartBin views
@api_view(['GET', 'POST'])
def smartbin_list(request):
    if request.method == 'GET':
        smartbins = SmartBin.objects.all()
        serializer = SmartBinSerializer(smartbins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SmartBinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def smartbin_detail(request, pk):
    smartbin = get_object_or_404(SmartBin, pk=pk)

    if request.method == 'GET':
        serializer = SmartBinSerializer(smartbin)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SmartBinSerializer(smartbin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = SmartBinSerializer(smartbin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        smartbin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Waste views
@api_view(['GET', 'POST'])
def add_waste(request):
    if request.method == 'GET':
        waste = Waste.objects.all()
        serializer = WasteSerializer(waste, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WasteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

