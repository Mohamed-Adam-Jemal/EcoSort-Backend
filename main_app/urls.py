from django.urls import path
from .views import (
    wastebot_list, wastebot_detail,
    wastebin_list, wastebin_detail,
    user_list, user_detail, wastes_list, waste_detail, waste_stream
)

urlpatterns = [
    # User URLs
    path('users/', user_list, name='users-list'),
    path('users/<int:pk>/', user_detail, name='users-detail'),

    # WasteBot URLs
    path('wastebots/', wastebot_list, name='wastebots-list'),
    path('wastebots/<int:pk>/', wastebot_detail, name='wastebot-detail'),

    # WasteBins URLs
    path('wastebins/', wastebin_list, name='wastebins-list'),
    path('wastebins/<int:pk>/', wastebin_detail, name='wastebin-detail'),

    # Waste URLs
    path('waste/', wastes_list, name='wastes-list'),
    path('sse/waste/', waste_stream, name='waste_stream'),
    path('waste/<int:pk>/', waste_detail, name='waste-detail'),
]