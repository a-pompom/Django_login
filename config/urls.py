from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('custom_auth.urls')),
]

handler404 = 'custom_auth.views.handler404'