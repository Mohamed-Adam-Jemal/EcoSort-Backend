from rest_framework import serializers
from .models import Waste, SmartBin, WasteBot, User
from django.contrib.auth.hashers import make_password, check_password

# Serializer for the User model (optional, if you need to expose user data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
# Serializer for the SmartBin model
class SmartBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBin
        fields = '__all__'  # Serialize all fields in the SmartBin model

# Serializer for the TrashBot model
class WasteBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBot
        fields = '__all__'  # Serialize all fields in the TrashBot model

class SmartbinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBin
        fields = '__all__'  

# Serializer for the TrashBot model
class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = '__all__'  # Serialize all fields in the TrashBot model
