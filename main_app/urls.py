from django.urls import path
from .views import (
    wastebot_list, wastebot_detail,
    smartbin_list, smartbin_detail,
    add_waste, user_list, user_detail
)

urlpatterns = [
    # User URLs
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),

    # WasteBot URLs
    path('wastebots/', wastebot_list, name='wastebot-list'),
    path('wastebots/<int:pk>/', wastebot_detail, name='wastebot-detail'),

    # SmartBin URLs
    path('smartbins/', smartbin_list, name='smartbin-list'),
    path('smartbins/<int:pk>/', smartbin_detail, name='smartbin-detail'),

    # Waste URLs
    path('waste/', add_waste, name='add-waste'),
]