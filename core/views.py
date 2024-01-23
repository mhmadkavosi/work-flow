from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WorkFlow
from .serializer import WorkflowSerializer


@api_view(["GET"])
def get_workflows(request):
    workflows = WorkFlow.objects.prefetch_related('step_set').all()
    serializer = WorkflowSerializer(workflows, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_workflow(request, pk):
    query_set = get_object_or_404(WorkFlow, pk=pk)
    serializer = WorkflowSerializer(query_set)
    return Response(serializer.data)
