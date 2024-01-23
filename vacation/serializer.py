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


class PartialUpdateField(serializers.Field):
    """
    A custom serializer field for partial updates.
    Allows partial updates only for the specified fields.
    """

    def to_representation(self, value):
        """
        Return the value as is during serialization.
        """
        return value

    def to_internal_value(self, data):
        """
        Return the data as is during deserialization.
        """
        return data


class LeaveUpdateSerializer(serializers.ModelSerializer):
    status = PartialUpdateField()

    class Meta:
        model = Leave
        fields = ['status']


class LeaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['reason', 'start_date', 'end_date', 'user']

    def validate(self, data):
        """
           Custom validation to ensure start_date is less than end_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            return serializers.ValidationError("Start Date must be less than End Date.")

        return data
