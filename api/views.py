from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET',])
def login_view(request):

    return Response(data={"response":"everything is allright"})