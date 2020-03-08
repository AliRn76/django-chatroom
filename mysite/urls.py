"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

from chat.views import main_view, \
    singup_view, \
    profile_view, \
    private_chat_view, \
    myprofile_view ,\
    myprofile_edit_view, \
    logout_view


    # login_view, \
    # profiles_view, \
    # profile_edit_view, \
    # profile_delete_view, \
    # login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include("chat.urls")),
    path('game/', include("game.urls")),
    path('upload/', include("receiver.urls")),

    path('', main_view, name="main"),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', logout_view, name="logout"),
    path('signup/', singup_view, name="singup"),
    path('profile/<str:user_username>', profile_view, name="profile"),
    path('myprofile/', myprofile_view, name="myprofile"),
    path('myprofile/edit', myprofile_edit_view, name="myprofile-edit"),
    path('private-chat/<int:pv_id>', private_chat_view, name="private-chat"),


    # path('login/', login_view, name="login"),
    # path('profiles/', profiles_view, name="profiles"),
    # path('profile/<int:my_id>/edit', profile_edit_view, name="profile_edit"),
    # path('profile/<int:my_id>/delete/', profile_delete_view, name="profile_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)