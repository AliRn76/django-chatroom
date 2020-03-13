from django.urls import path, include

from receiver.views import upload_view, delete_file_view

app_name = "upload"

urlpatterns =[
    path('api/', include('receiver.api.urls')),

    path('', upload_view, name="upload"),
    path('<int:file_number>/delete', delete_file_view, name="delete"),
    ]