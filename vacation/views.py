from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Leave
from .serializer import LeaveSerializer, LeaveUpdateStatusSerializer, LeaveCreateSerializer, LeaveUpdateSerializer


@api_view(["GET"])
def get_leaves(request):
    leaves = Leave.objects.all()
    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_leaves_info(request, pk):
    leaves = get_object_or_404(Leave, pk=pk)
    serializer = LeaveSerializer(leaves)
    return Response(serializer.data)


@api_view(["POST"])
def create_leaves(request):
    serializer = LeaveCreateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["PUT"])
def update_leave_status(request):
    leave = get_object_or_404(Leave, id=request.data.get("leave_id"))
    serializer = LeaveUpdateStatusSerializer(
        leave, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)

    serializer.save()
    return Response(serializer.data)


@api_view(["PUT"])
def update_leave_reason_date(request):
    leave = get_object_or_404(Leave, id=request.data.get("leave_id"))

    serializer = LeaveUpdateSerializer(leave, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)

    if not (('reason' in request.data) or ('start_date' in request.data) or ('end_date' in request.data)):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    leave.status = Leave.REQUEST_STATUS_PENDING
    leave.save()
    serializer.save()
    return Response(serializer.data)
