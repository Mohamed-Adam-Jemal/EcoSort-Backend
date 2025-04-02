from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    role = models.CharField(max_length=30, default="user")
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} | {self.first_name} {self.last_name} | {self.role}"

    def save(self, *args, **kwargs):
        # Hash the password before saving the model instance
        if self.password and not self.password.startswith('pbkdf2_sha256$'):  # Check if the password is not already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class WasteBot(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=20, default='Not Specified')  # Model of the WasteBot
    status = models.CharField(max_length=20, default='Inactive')  # Status (Active/Inactive)
    location = models.CharField(max_length=50)  
    autonomy = models.IntegerField()  

    def __str__(self):
        return f"WasteBot {self.id} - {self.model} ({self.status})"

class Waste(models.Model):
    id = models.AutoField(primary_key=True)
    waste_type = models.CharField(max_length=20)  # e.g., plastic, paper, metal, other
    time_collected = models.DateTimeField(auto_now_add=True)  # Timestamp of collection

    # Foreign Key to WasteBot
    wastebot = models.ForeignKey('WasteBot', on_delete=models.CASCADE)

    # Foreign Key to WastetBin (one-to-many relationship)
    WasteBin = models.ForeignKey('WasteBin', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Waste {self.waste_id} ({self.waste_type}) collected by WasteBot {self.wastebot.wastebot_id}"


class WasteBin(models.Model):

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    cover = models.CharField(max_length=20, default='Closed')  # Cover status (Open/Closed)
    location = models.CharField(max_length=20)
    capacity = models.IntegerField()
    fill_level = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)

    def __str__(self):
        return f"WasteBin {self.WasteBin_id} - {self.status}"




