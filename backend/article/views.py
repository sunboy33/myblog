import time
from datetime import timedelta

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q, Sum
from django.utils import timezone

from .models import ArticleMessage
from .serializers import ArticleMessageSerializer_, ArticleMessageSerializer
from categorie.models import ArticleType,ArticleLabel
from categorie.serializers import ArticleLabelSerializer
from media.models import WebViews
from backend.redis_client import redis_client
from backend.ai_client import generate_article_abstract



"""
@last-edit-date 2026-04-24
@author tyd
@desc 获取主页文章、更新网站访问量(埋点)

"""
@api_view(['GET'])
@permission_classes([])
def get_list_sort_article(request):
    # 获取请求IP
    remote_add = request.META.get('REMOTE_ADDR')
    now = timezone.now()

    # 更新访问记录（原子操作）
    view, created = WebViews.objects.get_or_create(
        ip=remote_add,
        defaults={'count': 1}
    )
    if not created:
        time_since_last_visit = now - view.latestTime
        if time_since_last_visit > timedelta(hours=24):
            view.count += 1
            view.latestTime = now
            view.save(update_fields=['count', 'latestTime'])

    # 获取总访问量
    webview = WebViews.objects.aggregate(total=Sum('count'))['total'] or 0

    # 按分类获取文章
    items = ArticleType.objects.order_by('priority').values('id', 'type')
    articleCount = ArticleMessage.objects.count()
    data = {}
    for item in items:
        articles = ArticleMessage.objects.filter(type_id=item['id']).order_by('-createtime')[:6]
        serializer = ArticleMessageSerializer_(articles, many=True)
        data[item['id']] = serializer.data

    return Response({
        "code": 200,
        "data": data,
        "articleCount": articleCount,
        "view": webview,
        "currentTimeMillis": int(time.time() * 1000)
    }, status=status.HTTP_200_OK)


""""
@last-edit-date 2026-04-24
@author tyd
@desc 获取主页推荐文章
"""
@api_view(['GET'])
@permission_classes([])
def get_recommend_articles(request):
    recommend_articles = ArticleMessage.objects.filter(recommend=True)
    recommend_articles_serializer = ArticleMessageSerializer_(recommend_articles, many=True)
    return Response(data={
        "code": 200,
        "currentTimeMillis": int(time.time() * 1000),
        "data": recommend_articles_serializer.data,
        "articleCount": len(recommend_articles)
    }, status=status.HTTP_200_OK)



"""
@last-edit-date 2026-04-27
@author tyd
@desc 根据id获取文章信息

"""
@api_view(['GET'])
@permission_classes([])
def get_article_by_id(request, id):
    article = ArticleMessage.objects.get(id=id)
    if request.GET.get("edit") is None:
        remote_add = request.META.get('REMOTE_ADDR')
        key = f"article:{id}:ip:{remote_add}"
        if redis_client.set(key, 1, nx=True, ex=86400):
            article.pageviews += 1
            article.save(update_fields=['pageviews'])
    serializer = ArticleMessageSerializer(article)
    return Response(data={
        "code": 200,
        "article": serializer.data,
        "currentTimeMillis": int(time.time() * 1000)
    }, status=status.HTTP_200_OK)




"""
@last-edit-date 2026-04-29
@author tyd
@desc 获取文章，分页

"""
@api_view(['GET'])
@permission_classes([])
def get_article_by_pagination(request):
    pageSize = int(request.GET.get('pageSize'))
    currentPage = int(request.GET.get('currentPage'))
    if request.GET.get('title') is None:
        count = ArticleMessage.objects.all().count()
        articles = ArticleMessage.objects.select_related('type').prefetch_related('label').all()[(currentPage - 1) * pageSize: currentPage * pageSize]
        serializer = ArticleMessageSerializer_(articles, many=True)
        for index, item in enumerate(serializer.data):
            item['s_id'] = index + 1 + (currentPage - 1) * pageSize
        return Response(data={
            "success": True,
            "count": count,
            "articles": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        is_recommend = request.GET.get("is_recommend")
        limit = request.GET.get('limit')
        sort = request.GET.get('sort')
        label = request.GET.get('label')
        title = request.GET.get('title')
        query = Q()
        if is_recommend:
            query &= Q(recommend=is_recommend)
        if limit:
            query &= Q(limit=limit)
        if sort:
            query &= Q(type__type=sort)
        if label:
            query &= Q(label__label=label)
        if title:
            title_query = Q(Q(title__icontains=title))
            query &= title_query
        count = ArticleMessage.objects.filter(query).count()
        articles = ArticleMessage.objects.filter(query)[(currentPage - 1) * pageSize: currentPage * pageSize]
        serializer = ArticleMessageSerializer_(articles, many=True)
        for index, item in enumerate(serializer.data):
            item['s_id'] = index + 1 + (currentPage - 1) * pageSize
        return Response(data={
            "success": True,
            "count": count,
            "articles": serializer.data
        }, status=status.HTTP_200_OK)


"""
@last-edit-date 2026-04-29
@author tyd
@desc 获取某一类型的所有文章

"""
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_article_by_type(request):
    label_id = request.GET.get('label_id')
    type_id = int(request.GET.get('type_id'))
    pageSize = int(request.GET.get('pageSize'))
    currentPage = int(request.GET.get('currentPage'))
    if label_id is None:
        count = ArticleMessage.objects.filter(type_id=type_id).count()
        articles = ArticleMessage.objects.filter(type_id=type_id).order_by(
            '-createtime')[(currentPage-1)* pageSize:currentPage*pageSize]
        labels = ArticleLabel.objects.filter(type_id=type_id)
        serializer = ArticleMessageSerializer_(articles, many=True)
        label_serializer = ArticleLabelSerializer(labels, many=True)
        return Response(data={
            "count": count,
            "articles": serializer.data,
            "tag_with_num": label_serializer.data
        }, status=status.HTTP_200_OK)
    else:
        count = ArticleMessage.objects.filter(
            type_id=type_id, label__id=label_id).count()
        articles = ArticleMessage.objects.filter(
            type_id=type_id, label__id=label_id).order_by('-createtime')
        labels = ArticleLabel.objects.filter(type_id=type_id)
        serializer = ArticleMessageSerializer_(articles, many=True)
        label_serializer = ArticleLabelSerializer(labels, many=True)
        return Response(data={
            "success": True,
            "count": count,
            "articles": serializer.data,
            "tag_with_num": label_serializer.data
        }, status=status.HTTP_200_OK)


"""添加文章"""
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_article(request):
    try:
        data = request.data
        data['type_id'] = ArticleType.objects.filter(type=data['type']).first().id
        label = data['label']
        del data['type']
        del data['label']

        text = data.get('text', '')
        abstract = generate_article_abstract(text)
        print("abstract:", abstract)
        print("cover:", data.get("cover"))
        data['abstract'] = abstract

        new_article = ArticleMessage.objects.create(**data)
        label_ids = ArticleLabel.objects.filter(
            label__in=label
        ).values_list('id', flat=True)
        new_article.label.set(label_ids)
        return Response({"code": 200, "currentTimeMillis": int(time.time() * 1000)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={
            "code": 500,
            "message": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_article(request, id):
    obj = ArticleMessage.objects.get(id=id)
    obj.delete()
    return Response({"success": True}, status=status.HTTP_200_OK)



"""修改文章信息"""
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_detail(request, id):
    try:
        data = request.data
        label = data['label']
        data['type_id'] = ArticleType.objects.filter(
            type=data['type']).first().id
        del data['label']
        del data['type']

        if 'text' in data:
            abstract = generate_article_abstract(data['text'])
            data['abstract'] = abstract

        ArticleMessage.objects.filter(id=id).update(**data)
        new_article = ArticleMessage.objects.get(id=id)
        label_ids = ArticleLabel.objects.filter(
            label__in=label
        ).values_list('id', flat=True)
        new_article.label.set(label_ids)
        return Response({"success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return Response(data={
            "success": False,
            "message": "文章修改失败!",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







