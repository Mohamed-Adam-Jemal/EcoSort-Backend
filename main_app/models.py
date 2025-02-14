from django.db import models
from django.contrib.auth.models import User

class Waste(models.Model):
    waste_id = models.AutoField(primary_key=True)
    waste_type = models.CharField(max_length=20)  # e.g., plastic, paper, metal, other
    time_collected = models.DateTimeField(auto_now_add=True)  # Timestamp of collection

    # Foreign Key to TrashBot
    wastebot = models.ForeignKey('WasteBot', on_delete=models.CASCADE)

    # Foreign Key to SmartBin (one-to-many relationship)
    smartbin = models.ForeignKey('SmartBin', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Waste {self.trash_id} ({self.trash_type}) collected by WasteBot {self.trashbot.trashbot_id}"


class SmartBin(models.Model):

    smartbin_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    capacity = models.IntegerField()
    fill_level = models.IntegerField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()

    def __str__(self):
        return f"SmartBin {self.smartbin_id} - {self.status}"


class WasteBot(models.Model):
    wastebot_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)  # e.g., active, idle, charging, maintenance
    location = models.CharField(max_length=20)  # GPS coordinates or address

    # Foreign Key to User (optional, if TrashBot is assigned to a user)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"WasteBot {self.trashbot_id} ({self.status})"
    

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)  
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=20) 
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=20, default='user')  
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id}:({self.username})"
    
