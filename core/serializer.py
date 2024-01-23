from rest_framework import serializers
from .models import WorkFlow, Step


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True, source='step_set')

    class Meta:
        model = WorkFlow
        fields = '__all__'
