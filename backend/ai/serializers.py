from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'messages', 'created_at', 'updated_at']


class CreateMessageSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    role = serializers.ChoiceField(choices=['user', 'assistant'])
    content = serializers.CharField()


class CreateSessionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False, default='新对话')
