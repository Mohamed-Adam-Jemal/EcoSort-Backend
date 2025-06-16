from django.contrib import admin
from django.urls import path, include
from main_app.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('', include('main_app.urls')),
]
