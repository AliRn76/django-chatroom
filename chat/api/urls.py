from django.urls import path, include

from chat.api.views import chat_api_view

app_name = "chat-api"

urlpatterns = [
    path('chat/', chat_api_view, name='chat'),

]