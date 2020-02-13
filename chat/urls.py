



from django.urls import path

from chat.views import chat_view, \
    chat_edit_view, \
    chat_delete_view

urlpatterns = [
    path('<int:room_id>/', chat_view, name="chat"),
    path('<int:room_id>/<int:msg_id>/edit', chat_edit_view, name="chat_edit"),
    path('<int:room_id>/<int:msg_id>/delete', chat_delete_view, name="chat_delete"),
]