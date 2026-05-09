from rest_framework import serializers
from article.models import ArticleMessage
from .models import ArticleType,ArticleLabel



class ArticleTypeSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()
    class Meta:
        model = ArticleType
        fields = ['id','type', 'desc','priority','article_count']
    
    def get_article_count(self, obj):
        return ArticleMessage.objects.filter(type=obj).count()



class ArticleLabelSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField()
    articleCount = serializers.SerializerMethodField()
    class Meta:
        model = ArticleLabel
        fields = ['id','label', 'desc','type_name','articleCount']

    def get_type_name(self, obj):
        return obj.type.type if obj.type else '未分类'

    def get_articleCount(self, obj):
        return obj.labels.count()
    


