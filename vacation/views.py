from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Leave
from .serializer import LeaveSerializer, LeaveUpdateSerializer, LeaveCreateSerializer


@api_view(["GET"])
def get_leaves(request):
    leaves = Leave.objects.all()
    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_leaves_info(request, id):
    leaves = get_object_or_404(Leave, id)
    serializer = LeaveSerializer(leaves)
    return Response(serializer.data)


@api_view(["POST"])
def create_leaves(request):
    serializer = LeaveCreateSerializer(request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data)


@api_view(["PUT"])
def update_leave_status(request):
    leave = get_object_or_404(Leave, id=request.data.get("leave_id"))
    serializer = LeaveUpdateSerializer(leave, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data)
