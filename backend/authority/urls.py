from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('code', get_au_code),
    path('refreshToken', TokenRefreshView.as_view()),
    path('verify', verify)
]
