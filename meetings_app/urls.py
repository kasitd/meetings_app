from django.contrib import admin
from django.urls import path, include
from meetings.views import home

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('meetings/', include('meetings.urls')),
    path('website/', include('django.contrib.auth.urls'))
]
