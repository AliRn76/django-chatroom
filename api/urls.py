from django.urls import path, include

from api.views import login_view
from rest_framework.authtoken.views import obtain_auth_token

app_name = "api"

urlpatterns = [
    path('login/', obtain_auth_token),
    path('test/', login_view, name="upload"),
]