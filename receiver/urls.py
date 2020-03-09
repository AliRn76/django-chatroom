from django.urls import path

from receiver.views import upload_view, delete_file_view

app_name = "upload"

urlpatterns = [
    path('', upload_view, name="upload"),
    path('<int:file_number>/delete', delete_file_view, name="delete"),

    ]