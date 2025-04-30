from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAgent, IsAdmin, IsUser
from rest_framework.response import Response
from rest_framework import status
from .models import WasteBot, WasteBin, Waste, User
from .serializers import WasteBotSerializer, WasteBinSerializer, WasteSerializer, UserSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .aws_iot_core_config import publish_wastebot_status


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

        # Add custom claims to the access token
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

from django.http import StreamingHttpResponse
import json
import time
from asgiref.sync import sync_to_async

from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async
import asyncio
import json
from .models import Waste  # Import your model
from .serializers import WasteSerializer  # Import your serializer
from .signals import new_waste_queue

async def waste_stream(request):
    """
    Stream waste data to the client using Server-Sent Events (SSE).
    
    """
    async def event_stream():
        """
        Asynchronous generator function that continuously:
        1. Waits for new data from the queue (blocking operation)
        2. Formats the data as an SSE-compliant message
        3. Yields the formatted message to the client
        
        The loop runs indefinitely until the client disconnects.
        """
        while True:
            # Wait for new data from the queue (asynchronous operation)
            # This will block the coroutine until new data arrives
            new_waste_data = await new_waste_queue.get()
            
            # Format the data as an SSE message:
            # - 'data:' prefix is required by SSE protocol
            # - Double newline (\n\n) marks the end of an event
            # - JSON serialization ensures proper formatting of complex data
            yield f"data: {json.dumps(new_waste_data)}\n\n"

    # Create and configure the streaming response:
    # 1. Set content type to text/event-stream (required for SSE)
    # 2. Disable caching to ensure real-time updates
    # 3. Keep connection alive for persistent updates
    response = StreamingHttpResponse(
        event_stream(),  # The async generator that produces the stream
        content_type="text/event-stream"  # Mandatory SSE content type
    )
    
    # HTTP headers to optimize SSE behavior:
    response['Cache-Control'] = 'no-cache'  # Prevent caching of events
    response['Connection'] = 'keep-alive'   # Maintain persistent connection
    
    return response


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

    elif request.method in ['PUT', 'PATCH']:
        serializer = WasteBotSerializer(wastebot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Publish status change to MQTT
            if 'status' in request.data:
                # Convert Django model status to MQTT command
                wastebot_status = "ON" if request.data['status'] == "Active" else "OFF"
                publish_wastebot_status(wastebot_status)
            
            return Response(serializer.data)

    elif request.method == 'DELETE':
        # Verify that the user is an admin
        wastebot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# WasteBin views
@api_view(['GET', 'POST'])
def wastebin_list(request):
    if request.method == 'GET':
        WasteBins = WasteBin.objects.all()
        serializer = WasteBinSerializer(WasteBins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WasteBinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def wastebin_detail(request, pk):
    try:
        wastebin_instance = WasteBin.objects.get(pk=pk)  # Changed variable name
    except WasteBin.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WasteBinSerializer(wastebin_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WasteBinSerializer(wastebin_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = WasteBinSerializer(wastebin_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        wastebin_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# List all Waste objects or create a new Waste
@api_view(['GET'])
def wastes_list(request):
    if request.method == 'GET':
        waste = Waste.objects.all()
        serializer = WasteSerializer(waste, many=True)
        return Response(serializer.data)

# Retrieve, update, partial update or delete a single Waste object
@api_view(['GET'])
def waste_detail(request, pk):
    waste = get_object_or_404(Waste, pk=pk)

    if request.method == 'GET':
        serializer = WasteSerializer(waste)
        return Response(serializer.data)
