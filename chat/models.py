from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import datetime


User = settings.AUTH_USER_MODEL


# class Profile(models.Model):
#     name        = models.CharField(max_length=100)
#     lastname    = models.CharField(max_length=100)
#     username    = models.CharField(max_length=20, null=True)
#     password    = models.CharField(max_length=20, null=True)
#     bio         = models.TextField()
#     datecreated = models.DateTimeField(auto_now=True)
#
#     def get_url_edit(self):
#         return reverse("profile_edit", kwargs={"my_id" : self.id})
#
#     def get_url_delete(self):
#         return reverse("profile_delete", kwargs={"my_id" : self.id})
#     #
#     # def get_url_profiles(self):
    #     print("he go it")
    #     return reverse("profiles")

# ####################################################################################
#
# class PV(models.Model):
#     user1       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     user2       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     datetime    = models.DateTimeField(blank=True)
#
#     def __str__(self):
#         return str(self.user1) + " - " + str(self.user2)
#

####################################################################################

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
    message     = models.TextField(null=True)
    roomid      = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    datetime    = models.DateTimeField(blank=True)
    unread      = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username) + "     : " + str(self.message) + "     roomid: " + str(self.roomid_id)+ "     unread: " + str(self.unread)

    def get_url_edit(self):
        return reverse("chat_edit", kwargs={"msg_id" : self.id, "room_id" : self.roomid_id})

    def get_url_delete(self):
        return reverse("chat_delete", kwargs={"msg_id" : self.id, "room_id" : self.roomid_id})


####################################################################################

class Members(models.Model):
    userid        = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    roomid        = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.userid) + "        roomid: " + str(self.roomid)
