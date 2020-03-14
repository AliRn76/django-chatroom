

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from receiver.models import Document

from receiver.api.serializers import DocumentSerializer

@api_view(['POST',])
@permission_classes((AllowAny,))
def upload_view(request):
    if request.method == "POST":
        data = {}
        print(request.data)
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            data['response'] = "that was good"
        else:
            data['response'] = "your file has problem"
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(data=data, )