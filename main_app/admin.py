from django.contrib import admin
from .models import Waste, WasteBin, WasteBot, User

admin.site.register(User)
admin.site.register(WasteBin)
admin.site.register(WasteBot)
admin.site.register(Waste)