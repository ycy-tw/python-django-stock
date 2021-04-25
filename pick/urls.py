from django.urls import path, include
from .views import PickView, DownloadPickResult


urlpatterns = [
    path('', PickView, name='pick'),
    path('download', DownloadPickResult, name='download'),
]