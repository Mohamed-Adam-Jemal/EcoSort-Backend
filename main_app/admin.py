from django.contrib import admin
from .models import Waste, SmartBin, WasteBot, User

admin.site.register(User)
admin.site.register(SmartBin)
admin.site.register(WasteBot)
admin.site.register(Waste)