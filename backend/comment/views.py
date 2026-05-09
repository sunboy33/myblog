import time

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import models
from .models import ArticleComment
from article.models import ArticleMessage

"""
@last-edit-date 2026-04-27
@author tyd
@desc 用户评论

"""
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, articleId):
    data = request.data
    ArticleComment.objects.create(time=timezone.now(), articleid=articleId, **data)
    ArticleMessage.objects.filter(id=articleId).update(comments=models.F('comments') + 1)
    return Response(data={"code": "200", "currentTimeMillis": int(time.time() * 1000)}, status=status.HTTP_200_OK)



"""
@last-edit-date 2026-04-27
@author tyd
@desc 获取文章评论

"""
@api_view(["GET"])
@permission_classes([])
def comment_list(request):
    article_id = request.GET.get("articleId")
    raw_query = """
                SELECT comment_articlecomment.id,articleid,content,fatherid,floorcommentid,time,users.userId userid,userName,avatar
                FROM comment_articlecomment,users
                where comment_articlecomment.authorid=users.UserId and articleid=%s
                ORDER BY comment_articlecomment.id;
                """
    comments = list(ArticleComment.objects.raw(raw_query, [article_id]))
    recordNum = len(comments)

    floor_comments_dict = {}
    child_comments_by_floor = {}
    for comment in comments:
        base = {
            "id": comment.id,
            "content": comment.content,
            "createtime": comment.time,
            "userid": comment.userid,
            "username": comment.userName,
            "avatar": comment.avatar,
            "parentid": comment.fatherid,
            "floorcommentid": comment.floorcommentid
        }
        if comment.floorcommentid == -1:
            base["childComments"] = {"total": 0, "records": []}
            floor_comments_dict[comment.id] = base
        else:
            parent = floor_comments_dict.get(comment.floorcommentid)
            if parent:
                base["parentUserId"] = parent["userid"]
                base["parentUserName"] = parent["username"]
                base["parentCommentId"] = base["parentid"]
                parent["childComments"]["records"].append(base)
                parent["childComments"]["total"] += 1
            else:
                if comment.floorcommentid not in child_comments_by_floor:
                    child_comments_by_floor[comment.floorcommentid] = []
                child_comments_by_floor[comment.floorcommentid].append(base)

    floor_comment_data = list(floor_comments_dict.values())
    for fc in floor_comment_data:
        if fc["id"] in child_comments_by_floor:
            for child in child_comments_by_floor[fc["id"]]:
                child["parentUserId"] = fc["userid"]
                child["parentUserName"] = fc["username"]
                child["parentCommentId"] = child["parentid"]
                fc["childComments"]["records"].append(child)
                fc["childComments"]["total"] += 1

    return Response(data={
        "recordNum": recordNum,
        "records": floor_comment_data
    }, status=status.HTTP_200_OK)

