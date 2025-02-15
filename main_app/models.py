from django.db import models
from django.contrib.auth.models import User

class Waste(models.Model):
    id = models.AutoField(primary_key=True)
    waste_type = models.CharField(max_length=20)  # e.g., plastic, paper, metal, other
    time_collected = models.DateTimeField(auto_now_add=True)  # Timestamp of collection

    # Foreign Key to TrashBot
    wastebot = models.ForeignKey('WasteBot', on_delete=models.CASCADE)

    # Foreign Key to SmartBin (one-to-many relationship)
    smartbin = models.ForeignKey('SmartBin', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Waste {self.waste_id} ({self.waste_type}) collected by WasteBot {self.wastebot.wastebot_id}"


class SmartBin(models.Model):

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    capacity = models.IntegerField()
    fill_level = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)

    def __str__(self):
        return f"SmartBin {self.smartbin_id} - {self.status}"


class WasteBot(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=20, default='Not Specified')  # Model of the WasteBot
    status = models.CharField(max_length=20, default='Inactive')  # Status (Active/Inactive)
    location = models.CharField(max_length=50)  # GPS coordinates or address
    autonomy = models.IntegerField()  # Battery autonomy in hours (default to 0)

    def __str__(self):
        return f"WasteBot {self.id} - {self.model} ({self.status})"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20) 
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30, default='user')  
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id},({self.username} is a {self.role})"
    

