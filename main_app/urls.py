from django.urls import path
from .views import (
    wastebot_list, wastebot_detail,
    smartbin_list, smartbin_detail,
    user_list, user_detail, wastes_list, waste_detail
)

urlpatterns = [
    # User URLs
    path('users/', user_list, name='users-list'),
    path('users/<int:pk>/', user_detail, name='users-detail'),

    # WasteBot URLs
    path('wastebots/', wastebot_list, name='wastebots-list'),
    path('wastebots/<int:pk>/', wastebot_detail, name='wastebot-detail'),

    # SmartBin URLs
    path('smartbins/', smartbin_list, name='smartbins-list'),
    path('smartbins/<int:pk>/', smartbin_detail, name='smartbin-detail'),

    # Waste URLs
    path('wastes/', wastes_list, name='wastes-list'),
    path('wastes/<int:pk>/', waste_detail, name='waste-detail'),
]