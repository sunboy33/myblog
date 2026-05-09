from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    register = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = User
        fields = ['userId','userName', 'phone','email', 'status','userSex','avatar','introduce','userType','register']



