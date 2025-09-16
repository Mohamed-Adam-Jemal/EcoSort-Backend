from django.contrib import admin
from django.urls import path, include
from main_app.views import user_login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('', include('main_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
