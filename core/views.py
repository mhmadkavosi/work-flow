from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WorkFlow, Step
from .serializer import WorkflowSerializer, StepSerializer


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


@api_view(['POST'])
def create_workflow(request):
    serializer = WorkflowSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_step(request):
    workflow_id = request.data.get("workflow_id")
    workflow = get_object_or_404(WorkFlow, id=workflow_id)

    step_data = {'workflow': workflow_id, **request.data}

    last_step = Step.objects.filter(
        workflow=workflow).order_by('-step_number').first()

    step_number = last_step.step_number + 1 if last_step else 0

    step_data['step_number'] = step_number

    step_serializer = StepSerializer(data=step_data)

    if not step_serializer.is_valid():
        return Response(step_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    step_serializer.save()
    return Response(step_serializer.data,
                    status=status.HTTP_201_CREATED)
