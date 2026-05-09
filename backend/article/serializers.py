from rest_framework import serializers
from .models import ArticleMessage


class ArticleMessageSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    type = serializers.CharField(source='type.type', read_only=True)
    createtime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    finalltime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = ArticleMessage
        fields = ['id','author', 'title','type','label','limit','pageviews','cover','show','comment','recommend','comments','createtime','finalltime','text']
    
    def get_label(self, obj):
        return list(obj.label.values_list('label', flat=True))
    

class ArticleMessageSerializer_(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    type = serializers.CharField(source='type.type', read_only=True)
    createtime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = ArticleMessage
        fields = ['id','author', 'title','type','label','limit','pageviews','cover','show','comment','recommend','comments','createtime', 'abstract']
    
    def get_label(self, obj):
        return list(obj.label.values_list('label', flat=True))