from django.urls import path
from .views import *


urlpatterns = [
    path('', user_list),
    path('<int:id>', user_detail),
    path('login', login),
    path('register', register),
    path('updateUserStatuts', update_user_statuts)
]