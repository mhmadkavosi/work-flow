from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WorkFlow, Step, Requests
from .serializer import WorkflowSerializer, StepSerializer, RequestCreateSerializer, RequestUpdateStatusSerializer, RequestSerializer
from vacation.models import Leave
from vacation.serializer import LeaveUpdateStatusSerializer


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

    serializer.is_valid(raise_exception=True)

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

    step_serializer.is_valid(raise_exception=True)

    step_serializer.save()
    return Response(step_serializer.data,
                    status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_request(request):
    workflow_id = request.data.get("workflow_id")
    workflow = get_object_or_404(WorkFlow, id=workflow_id)

    first_step = Step.objects.filter(
        workflow=workflow).order_by('step_number').first()

    request_data = {'workflow': workflow_id,
                    'step': first_step.id, 'user': first_step.user_owner, **request.data}

    request_serializer = RequestCreateSerializer(data=request_data)

    request_serializer.is_valid(raise_exception=True)

    request_serializer.save()

    return Response(request_serializer.data,
                    status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_request_status(requests):
    request = get_object_or_404(Requests, id=requests.data.get("request_id"))
    if (request.status == Requests.REQUEST_STATUS_REJECT or request.status == Requests.REQUEST_STATUS_ACCEPT):
        return Response(status=status.HTTP_200_OK, data={"status": request.status})

    current_step = get_object_or_404(Step, id=request.step_id)

    next_step = Step.objects.filter(
        workflow=request.workflow_id, step_number=current_step.step_number + 1).first()

    if next_step:
        request_update_data = {"step": next_step.id,
                               "status": Requests.REQUEST_STATUS_NEXT, "user": next_step.user_owner_id, "reason": requests.data.get("reason")}
        serializer = RequestUpdateStatusSerializer(
            request, data=request_update_data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    else:
        # update status of vacation to accept
        leave = get_object_or_404(Leave, id=request.leave_id)
        leave_serializer = LeaveUpdateStatusSerializer(
            leave, data={
                "status": Requests.REQUEST_STATUS_ACCEPT, "reason": requests.data.get("reason")}, partial=True)

        leave_serializer.is_valid(raise_exception=True)
        leave_serializer.save()

        request_update_data = {
            "status": Requests.REQUEST_STATUS_ACCEPT}

        serializer = RequestUpdateStatusSerializer(
            request, data=request_update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@api_view(["PUT"])
def reject_request_status(request):
    request = get_object_or_404(Requests, id=request.data.get("request_id"))
    if (request.status == Requests.REQUEST_STATUS_REJECT or request.status == Requests.REQUEST_STATUS_ACCEPT):
        return Response(status=status.HTTP_200_OK, data={"status": request.status})

    # update status of vacation to reject
    leave = get_object_or_404(Leave, id=request.leave_id)
    leave_serializer = LeaveUpdateStatusSerializer(
        leave, data={
            "status": Leave.REQUEST_STATUS_REJECT, "reason": request.data.get("reason")}, partial=True)

    leave_serializer.is_valid(raise_exception=True)
    leave_serializer.save()

    request_update_data = {
        "status": Requests.REQUEST_STATUS_REJECT}

    serializer = RequestUpdateStatusSerializer(
        request, data=request_update_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_all_request(request):
    requests = Requests.objects.all()
    serializer = RequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
def rollback_request(requests):
    request = get_object_or_404(Requests, id=requests.data.get("request_id"))
    if (request.status == Requests.REQUEST_STATUS_REJECT or request.status == Requests.REQUEST_STATUS_ACCEPT):
        return Response(status=status.HTTP_200_OK, data={"status": request.status})

    current_step = get_object_or_404(Step, id=request.step_id)

    last_step = Step.objects.filter(
        workflow=request.workflow_id, step_number=current_step.step_number - 1).first()

    if last_step:
        request_update_data = {"step": last_step.id,
                               "status": Requests.REQUEST_STATUS_NEXT, "user": last_step.user_owner_id, "reason": requests.data.get("reason")}
        serializer = RequestUpdateStatusSerializer(
            request, data=request_update_data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
