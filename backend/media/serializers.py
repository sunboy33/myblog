from rest_framework import serializers
from .models import WebSiteSettings



class WebSettingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WebSiteSettings
        fields = ['title', 'poem', 'author', 'recordNumber', 'email', 'copyrightInformation', 'backgroundImg']
