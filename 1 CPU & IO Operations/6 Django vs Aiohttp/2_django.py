import time

from django.urls import path
from django.contrib import admin
from django.http import HttpResponse


def index(request):
    time.sleep(0.1)  # io bound operation simulation
    return HttpResponse(status=200, content='Hello World!')


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]
