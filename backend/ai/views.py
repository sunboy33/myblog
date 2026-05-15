from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from backend.ai_client import chat_with_ai_stream
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, CreateMessageSerializer, CreateSessionSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    message = request.data.get('message', '').strip()
    if not message:
        return Response({"code": 400, "message": "Message is required"}, status=400)

    history = request.data.get('history', [])

    response = StreamingHttpResponse(
        chat_with_ai_stream(message, history),
        content_type='text/plain'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """获取用户所有会话列表"""
    sessions = ChatSession.objects.filter(user=request.user)
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response({"code": 200, "data": serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request):
    """创建新会话"""
    serializer = CreateSessionSerializer(data=request.data)
    if serializer.is_valid():
        session = ChatSession.objects.create(
            user=request.user,
            title=serializer.validated_data.get('title', '新对话')
        )
        return Response({"code": 200, "data": {"id": session.id, "title": session.title}})
    return Response({"code": 400, "message": "Invalid data"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session(request, session_id):
    """获取指定会话详情"""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
        serializer = ChatSessionSerializer(session)
        return Response({"code": 200, "data": serializer.data})
    except ChatSession.DoesNotExist:
        return Response({"code": 404, "message": "Session not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_session(request, session_id):
    """删除会话"""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
        session.delete()
        return Response({"code": 200, "message": "Deleted"})
    except ChatSession.DoesNotExist:
        return Response({"code": 404, "message": "Session not found"}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_message(request):
    """保存消息到会话"""
    serializer = CreateMessageSerializer(data=request.data)
    if serializer.is_valid():
        session_id = serializer.validated_data.get('session_id')
        role = serializer.validated_data['role']
        content = serializer.validated_data['content']

        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user)

        # 如果是用户的第一条消息，自动设置会话标题
        if role == 'user' and session.title == '新对话':
            session.title = content[:20]  # 取前20个字符作为标题
            session.save()

        message = ChatMessage.objects.create(
            session=session,
            role=role,
            content=content
        )
        return Response({
            "code": 200,
            "data": {
                "session_id": session.id,
                "session_title": session.title,
                "message_id": message.id
            }
        })
    return Response({"code": 400, "message": "Invalid data"}, status=400)