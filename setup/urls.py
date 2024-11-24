
from django.contrib import admin
from django.urls import path, include
from GFSystem import urls


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include('GFSystem.urls')),
]
