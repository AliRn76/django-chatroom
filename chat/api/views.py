from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from chat.models import Chat

from chat.api.serializers import ChatSerializer

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def chat_api_view(request):
    if request.method == "GET":

        # Set Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        obj = Chat.objects.filter(roomid_id=1).order_by('datetime')
        for i in obj:
            i.time = i.datetime.time()


        if obj:
            result_page = paginator.paginate_queryset(obj, request)
            serializer = ChatSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

        #     data = {}
    #     print(request.data)
    #     serializer = DocumentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         data['response'] = "that was good"
    #     else:
    #         data['response'] = "your file has problem"
    # else:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    #     pass
    # return Response(data={'respose':'ok'})