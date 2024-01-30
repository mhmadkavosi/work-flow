from rest_framework import serializers
from .models import WorkFlow, Step, Requests


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"


class WorkflowSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True, source="step_set")

    class Meta:
        model = WorkFlow
        fields = "__all__"


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ["name", "desc", "workflow",
                  "step", "user", "reason", "leave"]


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


class RequestUpdateStatusSerializer(serializers.ModelSerializer):
    status = PartialUpdateField()

    class Meta:
        model = Requests
        fields = ['status', 'step', 'user']
