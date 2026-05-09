from django.db import models

##########文章分类表##########
class ArticleType(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    type = models.CharField(max_length=32,null=False,unique=True,verbose_name="分类名称")
    desc = models.CharField(max_length=128,null=True,verbose_name="分类描述")
    priority = models.IntegerField(verbose_name="分类优先级")

##########文章标签表##########
class ArticleLabel(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    label = models.CharField(max_length=64,null=False,verbose_name="文章标签")
    desc = models.CharField(max_length=128,null=True,verbose_name="标签描述")
    type = models.ForeignKey('ArticleType',null=True,on_delete=models.SET_NULL,related_name="types",verbose_name="所属类型")

