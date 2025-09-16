from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async
import asyncio
import json

from .permissions import IsAgent, IsAdmin, IsUser
from .models import WasteBot, WasteBin, Waste, User
from .serializers import WasteBotSerializer, WasteBinSerializer, WasteSerializer, UserSerializer
from .aws_iot_core_config import publish_wastebot_status
from .signals import new_waste_queue

# -----------------------
# User login
# -----------------------
@csrf_exempt
@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if check_password(password, user.password):
        refresh = RefreshToken.for_user(user)
        refresh["first_name"] = user.first_name
        refresh["last_name"] = user.last_name
        refresh["email"] = user.email
        refresh["role"] = user.role
        access_token = str(refresh.access_token)
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# -----------------------
# SSE waste stream
# -----------------------
async def waste_stream(request):
    async def event_stream():
        while True:
            new_waste_data = await new_waste_queue.get()
            yield f"data: {json.dumps(new_waste_data)}\n\n"

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream"
    )
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    return response


# -----------------------
# User views
# -----------------------
@csrf_exempt
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

@csrf_exempt
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


# -----------------------
# WasteBot views
# -----------------------
@csrf_exempt
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

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def wastebot_detail(request, pk):
    wastebot = get_object_or_404(WasteBot, pk=pk)
    if request.method == 'GET':
        serializer = WasteBotSerializer(wastebot)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = WasteBotSerializer(wastebot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if 'status' in request.data:
                wastebot_status = "ON" if request.data['status'] == "Active" else "OFF"
                topic = f"{wastebot.model}/status"
                publish_wastebot_status(topic, wastebot_status)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        wastebot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------
# WasteBin views
# -----------------------
@csrf_exempt
@api_view(['GET', 'POST'])
def wastebin_list(request):
    if request.method == 'GET':
        wastebins = WasteBin.objects.all()
        serializer = WasteBinSerializer(wastebins, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WasteBinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def wastebin_detail(request, pk):
    wastebin_instance = get_object_or_404(WasteBin, pk=pk)
    if request.method == 'GET':
        serializer = WasteBinSerializer(wastebin_instance)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        partial = True if request.method == 'PATCH' else False
        serializer = WasteBinSerializer(wastebin_instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        wastebin_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------
# Waste views
# -----------------------
@api_view(['GET'])
def wastes_list(request):
    waste = Waste.objects.all()
    serializer = WasteSerializer(waste, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def waste_detail(request, pk):
    waste = get_object_or_404(Waste, pk=pk)
    serializer = WasteSerializer(waste)
    return Response(serializer.data)
