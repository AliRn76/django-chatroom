

from django.urls import path

from receiver.api.views import upload_view

app_name = "api"

urlpatterns = [
    path('send/', upload_view, name="chat"),
]