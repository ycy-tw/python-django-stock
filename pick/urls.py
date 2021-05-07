from django.urls import path, include
from .views import pick_view, download_pick_result

urlpatterns = [
    path('', pick_view, name='pick'),
    path('download', download_pick_result, name='download'),
]
