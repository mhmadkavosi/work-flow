from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Leave


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name']


class LeaveSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Leave
        fields = '__all__'
