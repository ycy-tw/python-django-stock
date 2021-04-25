from django.urls import path, include
from .views import (
    BasicVariableView,
)

urlpatterns = [
    # path('<int:symbol>/<str:variable>/', BasicVariableView, name='info'),
    path('<int:symbol>/', BasicVariableView, name='info'),
]
