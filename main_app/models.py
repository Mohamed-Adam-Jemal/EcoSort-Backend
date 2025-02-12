from django.db import models

class SmartBin(models.Model):
    smartbin_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)  # e.g., active, full, maintenance
    location = models.CharField(max_length=20)  # GPS coordinates or address
    capacity = models.IntegerField()  # Maximum capacity of the bin
    fill_level = models.IntegerField()  # Current fill level (percentage or weight)
    temperature = models.IntegerField()  # Temperature inside the bin
    humidity = models.IntegerField()  # Humidity inside the bin

    # Foreign Key to Trash (optional, if needed)
    trash = models.ForeignKey('Trash', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"SmartBin {self.smartbin_id} at {self.location}"
    

class Trash(models.Model):
    trash_id = models.AutoField(primary_key=True)
    trash_type = models.CharField(max_length=20)  # e.g., plastic, paper, metal, other
    time_collected = models.DateTimeField(auto_now_add=True)  # Timestamp of collection
    weight = models.FloatField()  # Weight of the trash (optional)
    confidence_score = models.FloatField()  # Confidence score from YOLO classification (optional)

    # Foreign Key to TrashBot
    trashbot = models.ForeignKey('TrashBot', on_delete=models.CASCADE)

    def __str__(self):
        return f"Trash {self.trash_id} ({self.trash_type}) collected by TrashBot {self.trashbot.trashbot_id}"
    


class TrashBot(models.Model):
    trashbot_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)  # e.g., active, idle, charging, maintenance
    location = models.CharField(max_length=20)  # GPS coordinates or address
    battery_level = models.IntegerField()  # Battery level (percentage)
    last_maintenance = models.DateTimeField()  # Timestamp of last maintenance

    # Foreign Key to User (optional, if TrashBot is assigned to a user)
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"TrashBot {self.trashbot_id} ({self.status})"
    