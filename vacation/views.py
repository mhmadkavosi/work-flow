from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Leave
from .serializer import LeaveSerializer


@api_view(["GET"])
def get_leaves(request):
    leaves = Leave.objects.all()
    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)
