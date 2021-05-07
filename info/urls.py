from django.urls import path, include
from .views import (
    basic_variable_view,
)

urlpatterns = [
    path('<int:symbol>/', basic_variable_view, name='info'),
]
