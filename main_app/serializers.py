from rest_framework import serializers
from .models import Waste, SmartBin, WasteBot, User
from django.contrib.auth.hashers import make_password, check_password

# Serializer for the Trash model
class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = '__all__'  # Serialize all fields in the Trash model

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

# Serializer for the User model (optional, if you need to expose user data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before creating the user
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)

        # Call the parent create method to save the user
        return super().create(validated_data)
class wastebotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBot
        fields = '__all__' 

class smartbinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBin
        fields = '__all__'  