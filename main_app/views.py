from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import WasteBot, SmartBin, Waste, User
from .serializers import WasteBotSerializer, SmartBinSerializer, WasteSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly

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

@api_view(['GET', 'PUT', 'DELETE'])
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
    
