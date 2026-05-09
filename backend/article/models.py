from django.db import models



##########文章信息表##########
class ArticleMessage(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    author = models.CharField(max_length=32, null=False, verbose_name="文章作者")
    title = models.CharField(max_length=32,null=False,unique=True,verbose_name="文章标题")
    type = models.ForeignKey('categorie.ArticleType',null=True,on_delete=models.SET_NULL,related_name="articles",verbose_name="文章类型")
    label = models.ManyToManyField('categorie.ArticleLabel',related_name="labels",verbose_name="文章标签")
    limit = models.CharField(max_length=16,null=False,verbose_name="文章权限")
    pageviews = models.IntegerField(default=0,verbose_name="浏览量")
    cover = models.URLField(null=True,verbose_name="文章封面")
    show = models.BooleanField(default=True,null=False,verbose_name="是否展示")
    comment = models.BooleanField(default=True,null=False,verbose_name="是否评论")
    recommend = models.BooleanField(default=True,null=False,verbose_name="是否推荐")
    comments = models.IntegerField(default=0,verbose_name="评论数")
    abstract = models.CharField(max_length=500, default='', verbose_name="文章摘要")
    createtime = models.DateTimeField(null=False,verbose_name="创建时间")
    finalltime = models.DateTimeField(null=True,auto_now_add=False,verbose_name="最终修改时间")
    text = models.TextField(verbose_name="文章内容")

    def delete(self, *args, **kwargs):
        # 先获取关联的标签
        labels = list(self.label.all())
        
        # 执行删除
        super().delete(*args, **kwargs)
        
        # 清理无用的标签
        for label in labels:
            if label.labels.count() == 0:
                label.delete()
