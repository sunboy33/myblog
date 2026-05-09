from django.db import models

##########文章评论##########
class ArticleComment(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="评论ID")
    articleid = models.IntegerField(verbose_name="文章id")
    authorid = models.IntegerField(verbose_name="评论作者的id")
    content = models.CharField(max_length=200,verbose_name="评论内容")
    fatherid= models.IntegerField(verbose_name="父评论id")
    floorcommentid = models.IntegerField(verbose_name="一级评论id")
    time = models.DateField(null=False,verbose_name="评论时间")
