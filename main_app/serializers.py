from rest_framework import serializers
from .models import Waste, WasteBin, WasteBot, User
from django.contrib.auth.hashers import make_password, check_password

# Serializer for the User model (optional, if you need to expose user data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
# Serializer for the WasteBin model
class WasteBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBin
        fields = '__all__'  # Serialize all fields in the WasteBin model

# Serializer for the TrashBot model
class WasteBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBot
        fields = '__all__'  # Serialize all fields in the TrashBot model

class WasteBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBin
        fields = '__all__'  

# Serializer for the TrashBot model
class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = '__all__'  # Serialize all fields in the TrashBot model
