from django.urls import path

from receiver.views import model_form_upload

app_name = "upload"

urlpatterns = [
    path('', model_form_upload, name="upload"),

    ]