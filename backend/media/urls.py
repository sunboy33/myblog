from django.urls import path
from .views import upload, web_setting, delete_media



urlpatterns = [
    path('upload', upload),
    path('webSettings', web_setting),
    path('', delete_media)
]


