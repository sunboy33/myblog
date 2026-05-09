from django.urls import path
from .views import *


urlpatterns = [
    path('operation', type_crud),
    path('label', label_crud),
    path('<int:id>', delete_sort)
]