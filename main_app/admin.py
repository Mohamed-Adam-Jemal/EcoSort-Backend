from django.contrib import admin
from .models import Waste, SmartBin, WasteBot

admin.site.register(Waste)
admin.site.register(SmartBin)
admin.site.register(WasteBot)