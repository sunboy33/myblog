from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('history', views.get_history, name='history'),
    path('session', views.create_session, name='create_session'),
    path('session/<int:session_id>', views.get_session, name='get_session'),
    path('session/<int:session_id>/delete', views.delete_session, name='delete_session'),
    path('message', views.save_message, name='save_message'),
]
