from rest_framework import serializers
from .models import Waste, WasteBin, WasteBot, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
# Serializer for the WasteBin model
class WasteBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBin
        fields = '__all__'  

# Serializer for the TrashBot model
class WasteBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBot
        fields = '__all__'  

# Serializer for the TrashBot model
class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = '__all__'  # Serialize all fields in the TrashBot model
