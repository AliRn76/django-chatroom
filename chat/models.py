from django.db import models
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import datetime


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    roomname    = models.CharField(max_length=20, null=True, blank=True)
    membercount = models.IntegerField(blank=True, null=True)
    pv          = models.BooleanField(default=False)
    unredcount  = models.IntegerField(default=0)

    def __str__(self):
        return "RoomID: " + str(self.id)

####################################################################################

class Chat(models.Model):
    user        = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    message     = models.TextField(null=True, blank=True)
    roomid      = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    datetime    = models.DateTimeField(blank=True)
    unread      = models.BooleanField(default=False)
    image       = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return str(self.user.username) + "     : " + str(self.message) + "     roomid: " + str(self.roomid_id)+ "     unread: " + str(self.unread)

    def get_url_edit(self):
        return reverse("chat_edit", kwargs={"msg_id" : self.id, "room_id" : self.roomid_id})

    def get_url_pv_edit(self):
        return reverse("private-chat_edit", kwargs={"msg_id" : self.id, "pv_id" : self.roomid_id})

    def get_url_delete(self):
        return reverse("chat_delete", kwargs={"msg_id" : self.id, "room_id" : self.roomid_id})


####################################################################################

class Members(models.Model):
    userid        = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    roomid        = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.userid) + "        roomid: " + str(self.roomid)


####################################################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
