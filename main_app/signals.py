# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Waste
import asyncio
from .serializers import WasteSerializer


# Create a queue to hold new waste data
new_waste_queue = asyncio.Queue()

@receiver(post_save, sender=Waste)
def waste_post_save(sender, instance, created, **kwargs):
    if created:
        # Serialize the new waste object
        serializer = WasteSerializer(instance)
        # Put the serialized data into the queue
        new_waste_queue.put_nowait(serializer.data)