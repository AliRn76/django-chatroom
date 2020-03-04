from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils.datetime_safe import datetime
from django.db import connection
from django.contrib.auth import logout
from .models import Chat, Room, Members
from .forms import SingupForm, SendMessageModelForm, EditMessageModelForm, EditProfileForm, SendMessagePVModelForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .tools import tool_2


####################################################################################

class PrivateChat:
    def __init__(self, id, name, unread):
        self.id = id
        self.name = name
        self.unread = unread


####################################################################################

class Navbar:
    def pv_list(request):
        cursor  = connection.cursor()
        cursor2 = connection.cursor()
        cursor3 = connection.cursor()

        user_rooms_name = []
        unreads = []
        pv_list = []

        cursor.execute('''select chat_room.id 
                                FROM chat_room, chat_members, auth_user 
                                WHERE (auth_user.id =''' + str(request.user.id) + ''') 
                                        AND (auth_user.id = chat_members.userid_id)
                                        AND (chat_members.roomid_id = chat_room.id )
                                        AND (chat_room.PV = 1)''')
        user_rooms_id = cursor.fetchall()  # ID Room Hayi Ke User Tooshe

        user_rooms_id = [i[0] for i in user_rooms_id]

        for id in user_rooms_id:
            cursor2.execute('''select auth_user.username
                                    FROM chat_room, chat_members, auth_user 
                                    WHERE (auth_user.id = chat_members.userid_id)
                                            AND (chat_members.roomid_id = chat_room.id )
                                            AND (chat_room.id = ''' + str(id) + ''')''')
            name_rooms = cursor2.fetchall()  # Username , Room Hayi ke Taraf Tooshe
            name1_rooms = name_rooms[0]      # Name e Nafar Avale Too PV
            name2_rooms = name_rooms[1]      # Name e Nafar Dovom Too PV

            if name1_rooms[0] != request.user.username:     # Age Nafar Aval Too PV Khodam Naboodam
                user_rooms_name.append(name1_rooms[0])      # List Az Name PV Hayi Ke Dari
            else:
                user_rooms_name.append(name2_rooms[0])      # List Az Name PV Hayi Ke Dari


            cursor3.execute('''select DISTINCT SUM(unread)
                                        FROM (((chat_chat
                                            INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                            INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                            INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                        WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                                AND (chat_room.id = ''' + str(id) + ''')
                                                AND (chat_chat.user_id = auth_user.id)''')
            temp_unreads = cursor3.fetchall()   # Tedad Unread Ha Ro Mikhad Hesab Kone
            unread = temp_unreads[0]
            unread = unread[0]
            if unread == None:
                unreads.append(0)               # Age Message Unread Nadasht ---> 0 Bezar
            else:
                unreads.append(unread)          # Age Message Unread Dasht   ---> Khode Adad Ro Bezar


        for i in range(len(user_rooms_name)):
            pv = PrivateChat(id     = user_rooms_id[i],
                             name   = user_rooms_name[i],
                             unread = unreads[i])           # Har Dafe Ye Instance Az PV Misaze
            pv_list.append(pv)                              # Ye List Az PV Ha

        return pv_list


    def sum_unreads(pv_list):
        sum_unreads = 0
        for i in pv_list:
            sum_unreads = sum_unreads + i.unread            # Kolle PM Haye Unread Ro Hesab Mikone

        return sum_unreads


####################################################################################

def main_view(request):
    try:
        print("Hello " + request.user.username)
        pv_list = Navbar.pv_list(request)
        sum_unreads = Navbar.sum_unreads(pv_list)

        context = {
            "pv_list": pv_list,
            "sum_unreads": sum_unreads,
            "name": request.user.first_name,
        }

    except:
        return render(request, "login.html", {})

    return render(request, "main.html", context)


####################################################################################

def logout_view(request):
    print("Bye " + request.user.username)
    logout(request)
    return redirect("../")


####################################################################################

def singup_view(request):
    user = User
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get("name")
            user.last_name  = form.cleaned_data.get("lastname")
            user.username   = form.cleaned_data.get("username")
            user.password   = form.cleaned_data.get("password")
            user.objects.create_user(user.username, "", user.password, first_name=user.first_name, last_name=user.last_name, is_staff=True)

            return redirect("../login")
    else:
        form = SingupForm()

    context = {
        "form" : form
    }
    return render(request, "signup.html", context)


####################################################################################

@login_required()
def chat_view(request, room_id):
    print(request.user.username + " Visited PublicChat ")
    if request.method == "POST":
        form = SendMessageModelForm(request.POST, request.FILES)

        if form.is_valid():
            object              = form.save(commit=False)
            object.user         = request.user
            object.datetime     = datetime.now()
            object.roomid_id    = room_id
            object.unread       = True
            if not (form.cleaned_data.get("message") == '' and form.cleaned_data.get("image") is None):
                print(request.user.username + " Send Message To PublicChat ---> " + form.cleaned_data.get("message"))
                object.save()

        form = SendMessageModelForm()
    else:
        form = SendMessageModelForm(request.FILES)

    obj = Chat.objects.filter(roomid_id = room_id).order_by('datetime')

    for i in obj:
        i.time = i.datetime.time()
        try:
            i.firstChar = i.message[0]
        except:
            i.firstChar = ''

    pv_list = Navbar.pv_list(request)
    sum_unreads = Navbar.sum_unreads(pv_list)

    context = {
        "obj": obj,
        "form": form,
        "tool_2": tool_2,
        "pv_list": pv_list,
        "user": request.user,
        "sum_unreads" : sum_unreads,
    }

    return render(request, "chat.html", context)


####################################################################################

@login_required()
def chat_edit_view(request, msg_id, room_id):
    try:
        message = Chat.objects.get(id=msg_id, roomid=room_id)

    except Chat.DoesNotExist:
        return render(request, 'error404.html')

    if request.user == message.user:
        print(request.user.username + " Trying To Edit " + str(message))
        if request.method == "POST":
            form = EditMessageModelForm(request.POST, instance=message)

            if form.is_valid():
                print(request.user.username + " Edited " + str(message) + " ---> " + form.cleaned_data.get("message"))
                form.save()

                return redirect("../")
        else:
            form = EditMessageModelForm(instance=message)

        obj = Chat.objects.filter(roomid=room_id).order_by('datetime')

        for i in obj:
            i.time = i.datetime.time()
            try:
                i.firstChar = i.message[0]
            except:
                i.firstChar = ''

        pv_list = Navbar.pv_list(request)
        sum_unreads = Navbar.sum_unreads(pv_list)

        context = {
            "obj": obj,
            "form": form,
            "tool_2": tool_2,
            "pv_list": pv_list,
            "user": request.user,
            "sum_unreads": sum_unreads,
        }

        return render(request, "chat.html", context)

    else:
        return render(request, 'error403.html')

####################################################################################

@login_required()
def chat_delete_view(request, msg_id, room_id):
    try:
        message = Chat.objects.get(id=msg_id, roomid=room_id)

    except Chat.DoesNotExist:
        return render(request, 'error404.html')
    if request.user == message.user:
        print(request.user.username + " Deleted " + str(message))
        message.delete()
        return redirect("../")
    else:
        return render(request, 'error403.html')

####################################################################################

@login_required()
def profile_view(request, user_username):
    try:
        user_id = User.objects.get(username=user_username).id
    except User.DoesNotExist:
        return render(request, 'error404.html')

    print(request.user.username + " Visited " + user_username + " Profile")

    object = User.objects.get(id=user_id)

    pv_list = Navbar.pv_list(request)
    sum_unreads = Navbar.sum_unreads(pv_list)

    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(user_id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_rooms_id = cursor.fetchall()  # ID Room Hayi Ke Taraf Tooshe


    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(request.user.id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    my_rooms_id = cursor.fetchall() # ID Room Hayi Ke Ma Toosh Hastim

    has_pv = False

    for room_id in user_rooms_id:
        if room_id in my_rooms_id:
            has_pv = True
            pv_id = room_id
            break


    if not has_pv:              # Age Ghabln Ba Ham PV Naraafte Bashan
        obj = Room.objects.create(membercount=2, pv=True)
        pv_id = obj.id          # New Room ID Baraye PV
        Members.objects.create(userid_id=request.user.id, roomid_id=pv_id)
        Members.objects.create(userid_id=user_id,         roomid_id=pv_id)
    else:
        pv_id = pv_id[0]        # Room ID Ke Ghabln Boode

    context = {
            "sum_unreads": sum_unreads,
            "pv_list" : pv_list,
            "pv_id" : pv_id,
            "obj" : object
        }
    return render(request, "profile.html", context)


####################################################################################

@login_required()
def myprofile_view(request):
    print(request.user.username + " Checked His Profile")
    object = User.objects.get(id=request.user.id)

    pv_list = Navbar.pv_list(request)
    sum_unreads = Navbar.sum_unreads(pv_list)

    context = {
        "sum_unreads": sum_unreads,
        "pv_list": pv_list,
        "obj" : object
    }
    return render(request, "myprofile.html", context)


####################################################################################

@login_required()
def myprofile_edit_view(request):
    obj = User.objects.get(id=request.user.id)
    lastobj = obj
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            obj.first_name = form.cleaned_data.get("name")
            obj.last_name = form.cleaned_data.get("lastname")
            obj.username = form.cleaned_data.get("username")
            obj.email = form.cleaned_data.get("email")
            obj.save()
            print(request.user.username + " Change His Profile From " +
                  lastobj.first_name + " " + lastobj.last_name  + " " + lastobj.username + " " + lastobj.email + " ---> " +
                  obj.first_name     + " " + obj.last_name      + " " + obj.username     + " " + obj.email)
            return redirect(".")

    else:
        initial_data = {
            "username": obj.username,
            "name":     obj.first_name,
            "lastname": obj.last_name,
            "email":    obj.email,
        }
        form = EditProfileForm(initial=initial_data)

    context = {
        "form": form
    }
    return render(request, "signup.html", context)


####################################################################################

@login_required()
def private_chat_view(request, pv_id):
    cursor = connection.cursor()
    cursor.execute('''select auth_user.username
                            FROM chat_room, chat_members, auth_user 
                            WHERE (auth_user.id = chat_members.userid_id)
                                    AND (chat_members.roomid_id = chat_room.id )
                                    AND (chat_room.id = ''' + str(pv_id) + ''')''')
    name_rooms = cursor.fetchall()   # Username , Room Hayi ke Taraf Tooshe
    name1_rooms = name_rooms[0]      # Name e Nafar Avale Too PV
    name2_rooms = name_rooms[1]      # Name e Nafar Dovom Too PV

    if name1_rooms[0] != request.user.username:     # Age Nafar Aval Too PV Khodam Naboodam
        pv_username = name1_rooms[0]      # List Az Name PV Hayi Ke Dari
    else:
        pv_username = name2_rooms[0]      # List Az Name PV Hayi Ke Dari

    print(request.user.username + " Trying To Send PV Message To " + pv_username )

    if request.method == "POST":
        form = SendMessageModelForm(request.POST, request.FILES)

        if form.is_valid():
            object              = form.save(commit=False)
            object.user         = request.user
            object.datetime     = datetime.now()
            object.roomid_id    = pv_id
            object.unread       = True
            if not (form.cleaned_data.get("message") == '' and form.cleaned_data.get("image") is None):
                print(request.user.username + " Send Message To " + pv_username + " ---> " + form.cleaned_data.get("message"))
                object.save()

        form = SendMessageModelForm()
    else:
        form = SendMessageModelForm(request.FILES)

    obj = Chat.objects.filter(roomid_id=pv_id).order_by('datetime')

    for i in obj:
        i.time = i.datetime.time()
        try:
            i.firstChar = i.message[0]
        except:
            i.firstChar = ''

    cursor3 = connection.cursor()
    cursor3.execute('''Update chat_chat 
                            Set unread=0
                            WHERE   NOT (user_id = ''' + str(request.user.id) + ''')
                                    AND (roomid_id =''' + str(pv_id) + ''')''')

    pv_list = Navbar.pv_list(request)
    sum_unreads = Navbar.sum_unreads(pv_list)

    context = {
        "obj": obj,
        "form": form,
        "tool_2": tool_2,
        "pv_list": pv_list,
        "user": request.user,
        "sum_unreads": sum_unreads,
    }

    return render(request, "chat.html", context)


####################################################################################
