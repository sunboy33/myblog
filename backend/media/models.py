from django.db import models


####网站配置#######
class WebSiteSettings(models.Model):
    title = models.CharField(max_length=32, null=False, verbose_name="网站标题")
    poem = models.CharField(max_length=128, null=False, verbose_name="诗句")
    author = models.CharField(max_length=32, null=False, verbose_name="网站作者")
    recordNumber = models.CharField(max_length=128, verbose_name="备案号")
    email = models.CharField(max_length=32, verbose_name="联系邮箱")
    copyrightInformation = models.CharField(max_length=128, verbose_name="版权信息")
    backgroundImg = models.CharField(max_length=128, verbose_name="背景图片")


class WebViews(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=32, null=False, verbose_name="访问ip")
    latestTime = models.DateTimeField(auto_now=True, verbose_name="最近一次访问网站的时间")
    count = models.IntegerField(verbose_name="该ip访问次数")

