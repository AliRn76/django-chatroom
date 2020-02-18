from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils.datetime_safe import datetime
from django.db import connection
from django.contrib.auth import logout
from chat.models import Chat, Room, Members
from .forms import SingupForm, SendMessageModelForm, EditMessageModelForm, EditProfileForm, SendMessagePVModelForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .tools import tool_2

class PrivateChat:
    def __init__(self, id, name, unread):
        self.id = id
        self.name = name
        self.unread = unread

'''
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                obj = Profile.objects.get(username=username)
                if obj.password == password:
                    print("hame chi ok e")
                    return redirect("../../../profiles")

                else:
                    print("password wrong bood")
            except:                                                    #error 404 ham mitone bede
                print("asan in user nadarim")
    context = {
        'form' : form
    }
    return render(request, "login.html", context)


####################################################################################
def profile_edit_view(request, my_id):
    obj = Profile.objects.get(id=my_id)
    # print("my_id: " + str(my_id))
    form = ProfileForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        form = ProfileForm()
    context = {
        'form' : form,
    }
    print(request.user)
    return render(request, "enterProfile.html", context)


###################################################

def profile_delete_view(request, my_id):
    obj = Profile.objects.get(id=my_id)
    if request.method == "POST":
        obj.delete()
        return redirect("../../../profiles")
    context = {
        "object" : obj
    }
    return render(request, "delete.html", context)

'''

####################################################################################

def main_view(request):
    try:
        cursor = connection.cursor()
        cursor.execute('''select chat_room.id 
                                FROM chat_room, chat_members, auth_user 
                                WHERE (auth_user.id =''' + str(request.user.id) + ''') 
                                        AND (auth_user.id = chat_members.userid_id)
                                        AND (chat_members.roomid_id = chat_room.id )
                                        AND (chat_room.PV = 1)''')
        user_id_rooms = cursor.fetchall()  # room haye PV ke taraf tooshoone

        user_id_rooms = [i[0] for i in user_id_rooms]

        user_name_rooms = []
        unreads = []
        for id in user_id_rooms:
            cursor = connection.cursor()
            cursor.execute('''select auth_user.username
                                    FROM chat_room, chat_members, auth_user 
                                    WHERE (auth_user.id = chat_members.userid_id)
                                            AND (chat_members.roomid_id = chat_room.id )
                                            AND (chat_room.id = ''' + str(id) + ''')''')
            name_rooms = cursor.fetchall()  # Username , Room Hayi ke Taraf Tooshe
            name1_rooms = name_rooms[0]
            name2_rooms = name_rooms[1]
            if name1_rooms[0] != request.user.username:
                user_name_rooms.append(name1_rooms[0])  # Username PV Ha i ke bahashon pv dari
            else:
                user_name_rooms.append(name2_rooms[0])  # pv name kasayi ke bahashon pv dari

            cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
            # cursor2.execute('''select SUM(unread)
            #                         FROM chat_room, chat_members, auth_user, chat_chat
            #                         WHERE   NOT (user_id = ''' + str(request.user.id) + ''')
            #                                 AND (chat_room.id = ''' + str(id) + ''')
            #                                 AND (auth_user.id = chat_members.userid_id)
            #                                 AND (chat_members.roomid_id = chat_room.id )
            #                                 AND (chat_chat.roomid_id = chat_room.id)''')
            cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
            cursor2.execute('''select DISTINCT SUM(unread)
                                        FROM (((chat_chat
                                            INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                            INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                            INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                        WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                                AND (chat_room.id = ''' + str(id) + ''')
                                                AND (chat_chat.user_id = auth_user.id)''')
            temp_unreads = cursor2.fetchall()
            unread = temp_unreads[0]
            unread = unread[0]
            if unread == None:
                unreads.append(0)
            else:
                unreads.append(unread)  # List Az PV Ha Va Unread Hashon

        pv_list = []
        for i in range(len(user_name_rooms)):
            pv = PrivateChat(id=user_id_rooms[i], name=user_name_rooms[i],
                             unread=unreads[i])  # har dafe ye instance az pv misaze
            pv_list.append(pv)  # ye list az PV ha

        context = {
            "pv_list": pv_list,
            "name" : request.user.first_name,
            # "active" : True
        }
    except:
        context = {
            # "name" : "Guys",
             # "active": False
        }
        return render(request, "login.html", context)
    return render(request, "main.html",context)

####################################################################################

# def login_view(request):
#     print("ok")
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         post = User.objects.filter(username=username)
#         if post:
#             username = request.POST['username']
#             request.session['username'] = username
#             return redirect("../")
#         else:
#             return render(request, 'login.html', {})
#
#     return render(request, "login.html",{})
#

# def profile(request):
#     if request.session.has_key('username'):
#         posts = request.session['username']
#         query = User.objects.filter(username=posts)
#         return render(request, 'app_foldername / profile.html', {"query":query})
#     else:
#         return render(request, 'app_foldername/login.html', {})

####################################################################################

def logout_view(request):
    logout(request)
    return redirect("../")


####################################################################################

def singup_view(request):
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user = User
    form = SingupForm()
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get("name")
            user.last_name = form.cleaned_data.get("lastname")
            user.username = form.cleaned_data.get("username")
            user.password = form.cleaned_data.get("password")
            user.objects.create_user(user.username,"",user.password,first_name=user.first_name,last_name=user.last_name, is_staff=True)

            return redirect("../login")
            # user.save()
    form = SingupForm()
    context = {
        "form" : form
    }
    return render(request,"signup.html",context)

####################################################################################

@login_required()
def chat_view(request, room_id):
    form = SendMessageModelForm(request.POST or None)
    if form.is_valid():
        '''
        ## try to use ajax
        response_data = {}

        if request.POST.get('action') == 'post':
            # object = form.save(commit=False)
            # object.user = request.user
            # object.datetime = datetime.now()
            # object.save()

            message = form.cleaned_data.get("message")

            response_data['user'] = request.user
            response_data['datetime'] = datetime.now()
            response_data['message'] = request.POST.get('id_message')

            Chat.objects.create(user=request.user, message= message, datetime=datetime.now())
            return JsonResponse(response_data)

            # title = request.POST.get('title')
            # description = request.POST.get('description')
            #
            # response_data['title'] = title
            # response_data['description'] = description
            #
            # Post.objects.create(
            #     title=title,
            #     description=description,
            # )
            # return JsonResponse(response_data)

        ## end try to use ajax
'''


        ### ravesh 2
        object              = form.save(commit=False)
        object.user         = request.user
        object.datetime     = datetime.now()
        object.roomid_id    = room_id
        object.unread       = True
        object.save()
        ### end ravesh 2

        ### ravesh 1
        # message = form.cleaned_data.get("message")
        # Chat.objects.create(user=request.user, message= message, datetime=datetime.now())
        ### end ravesh 1

    obj = Chat.objects.filter(roomid_id = room_id).order_by('datetime')

    for i in obj:
        i.time = i.datetime.time()

    for i in obj:
        i.firstChar = i.message[0]

    form = SendMessageModelForm()


    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE (auth_user.id =''' + str(request.user.id) + ''') 
                                AND (auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_id_rooms = cursor.fetchall()   # room haye PV ke taraf tooshoone

    user_id_rooms = [i[0] for i in user_id_rooms]

    user_name_rooms = []
    unreads = []
    for id in user_id_rooms:
        cursor = connection.cursor()
        cursor.execute('''select auth_user.username
                            FROM chat_room, chat_members, auth_user 
                            WHERE (auth_user.id = chat_members.userid_id)
                                    AND (chat_members.roomid_id = chat_room.id )
                                    AND (chat_room.id = ''' + str(id) + ''')''')
        name_rooms = cursor.fetchall()  # Username , Room Hayi ke Taraf Tooshe
        name1_rooms = name_rooms[0]
        name2_rooms = name_rooms[1]
        if name1_rooms[0] != request.user.username:
            user_name_rooms.append(name1_rooms[0])   # Username PV Ha i ke bahashon pv dari
        else:
            user_name_rooms.append(name2_rooms[0])  # pv name kasayi ke bahashon pv dari

        cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
        cursor2.execute('''select DISTINCT SUM(unread)
                                FROM (((chat_chat
                                    INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                    INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                    INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                        AND (chat_room.id = ''' + str(id) + ''')
                                        AND (chat_chat.user_id = auth_user.id)''')
        temp_unreads = cursor2.fetchall()
        unread = temp_unreads[0]
        unread = unread[0]
        if unread == None:
            unreads.append(0)
        else:
            unreads.append(unread)  # List Az PV Ha Va Unread Hashon

    sum_unreads = 0
    pv_list = []
    for i in range(len(user_name_rooms)):
        pv = PrivateChat(id=user_id_rooms[i], name=user_name_rooms[i], unread=unreads[i])  # har dafe ye instance az pv misaze
        sum_unreads = sum_unreads + unreads[i]
        pv_list.append(pv)  # ye list az PV ha

    context = {
        "pv_list" : pv_list,
        "sum_unreads" : sum_unreads,
        "tool_2" : tool_2,
        "obj" : obj ,
        "form" : form ,
        "user" : request.user,
    }
    return render(request, "chat.html", context)


####################################################################################

@login_required()
def chat_edit_view(request, msg_id, room_id):
    message = Chat.objects.get(roomid=room_id, id=msg_id, user=request.user.id)
    if message: # else error 404
        form = EditMessageModelForm(request.POST or None, instance=message)

        if form.is_valid():
            form.save()
            return redirect("../")

        obj = Chat.objects.filter(roomid=room_id).order_by('datetime')

        for i in obj:
            i.time = i.datetime.time()

        for i in obj:
            i.firstChar = i.message[0]

        # form = EditMessageModelForm() # in age bashe , text ghabli replace nmishe

        context = {
            "tool_2": tool_2,
            "obj": obj,
            "form": form,
            "user": request.user,
        }

        return render(request, "chat.html", context)


####################################################################################

@login_required()
def chat_delete_view(request, msg_id, room_id):
    obj = Chat.objects.get(roomid=room_id, id=msg_id, user=request.user.id)
    if obj: # else error 404
        obj.delete()
        render(request, "chat-delete.html")
        return redirect("../")

####################################################################################

@login_required()
def profile_view(request, user_username):
    user_id = User.objects.get(username=user_username).id

    myuser_id = request.user.id

    object = User.objects.get(id=user_id)

    # members_id = Members.objects.filter(userid = user_id)
    # print(members_id) # ok MEMBER ID ro gerftam
    # room_id = Room.objects.filter(pv = True and id = )

    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(user_id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_id_rooms = cursor.fetchall()   # room haye PV ke taraf tooshoone


    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(myuser_id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    myuser_id_rooms = cursor.fetchall() # room haye PV ke ma toosh hastim

    has_pv = False

    for room in user_id_rooms:
        if room in myuser_id_rooms:
            has_pv = True
            pv_id = room
            break

    if not has_pv:  # age ghablan ba ham ta hala PV narafte bashan
        obj = Room.objects.create(membercount=2, pv=True)
        pv_id = obj.id  # new room id baraye pv
        Members.objects.create(userid_id=user_id, roomid_id=pv_id)
        Members.objects.create(userid_id=myuser_id, roomid_id=pv_id)
    else:
        pv_id = pv_id[0]    # room id ke ghablan boode


    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(request.user.id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_id_rooms = cursor.fetchall()   # room haye PV ke taraf tooshoone

    user_id_rooms = [i[0] for i in user_id_rooms]

    user_name_rooms = []
    unreads = []
    for id in user_id_rooms:
        cursor = connection.cursor()
        cursor.execute('''select auth_user.username
                            FROM chat_room, chat_members, auth_user 
                            WHERE (auth_user.id = chat_members.userid_id)
                                    AND (chat_members.roomid_id = chat_room.id )
                                    AND (chat_room.id = ''' + str(id) + ''')
                                    AND (chat_room.PV = 1)''')
        name_rooms = cursor.fetchall()
        # print(name_rooms)
        name1_rooms = name_rooms[0]
        name2_rooms = name_rooms[1]
        if name1_rooms[0] != request.user.username:
            # print(name1_rooms)
            # print(request.user.username)
            user_name_rooms.append(name1_rooms[0])   # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)
        else:
            # print(name2_rooms)
            user_name_rooms.append(name2_rooms[0])  # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)

        cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
        cursor2.execute('''select DISTINCT SUM(unread)
                                        FROM (((chat_chat
                                            INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                            INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                            INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                        WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                                AND (chat_room.id = ''' + str(id) + ''')
                                                AND (chat_chat.user_id = auth_user.id)''')
        temp_unreads = cursor2.fetchall()
        unread = temp_unreads[0]
        unread = unread[0]
        if unread == None:
            unreads.append(0)
        else:
            unreads.append(unread)  # List Az PV Ha Va Unread Hashon

    pv_list = []
    for i in range(len(user_name_rooms)):
        pv = PrivateChat(id=user_id_rooms[i], name=user_name_rooms[i], unread=unreads[i])  # har dafe ye instance az pv misaze
        pv_list.append(pv)  # ye list az PV ha
        # print(pv_list[i].id)
        # print(pv_list[i].name)

    context = {

        "pv_list" : pv_list,
        "pv_id" : pv_id,
        "obj" : object
    }
    return render(request, "profile.html", context)


####################################################################################

@login_required()
def myprofile_view(request):
    object = User.objects.get(id=request.user.id)

    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(request.user.id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_id_rooms = cursor.fetchall()  # room haye PV ke taraf tooshoone

    user_id_rooms = [i[0] for i in user_id_rooms]

    user_name_rooms = []
    unreads = []
    for id in user_id_rooms:
        cursor = connection.cursor()
        cursor.execute('''select auth_user.username
                            FROM chat_room, chat_members, auth_user 
                            WHERE (auth_user.id = chat_members.userid_id)
                                    AND (chat_members.roomid_id = chat_room.id )
                                    AND (chat_room.id = ''' + str(id) + ''')
                                    AND (chat_room.PV = 1)''')
        name_rooms = cursor.fetchall()
        # print(name_rooms)
        name1_rooms = name_rooms[0]
        name2_rooms = name_rooms[1]
        print(1)
        if name1_rooms[0] != request.user.username:
            # print(name1_rooms)
            # print(request.user.username)
            user_name_rooms.append(name1_rooms[0])  # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)
            print(2)
        else:
            print(3)
            # print(name2_rooms)
            user_name_rooms.append(name2_rooms[0])  # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)

        cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
        cursor2.execute('''select DISTINCT SUM(unread)
                                          FROM (((chat_chat
                                              INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                              INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                              INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                          WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                                  AND (chat_room.id = ''' + str(id) + ''')
                                                  AND (chat_chat.user_id = auth_user.id)''')
        temp_unreads = cursor2.fetchall()
        unread = temp_unreads[0]
        unread = unread[0]
        if unread == None:
            unreads.append(0)
        else:
            unreads.append(unread)  # List Az PV Ha Va Unread Hashon
    pv_list = []
    for i in range(len(user_name_rooms)):
        print(4)
        pv = PrivateChat(id=user_id_rooms[i], name=user_name_rooms[i], unread=unreads[i])  # har dafe ye instance az pv misaze
        pv_list.append(pv)  # ye list az PV ha

    context = {
        "pv_list": pv_list,
        "obj" : object
    }
    return render(request, "myprofile.html", context)

####################################################################################

@login_required()
def myprofile_edit_view(request):
    obj = User.objects.get(id=request.user.id)

    initial_data ={
        "username": obj.username,
        "name": obj.first_name,
        "lastname": obj.last_name,
        "email": obj.email,
    }

    form = EditProfileForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        obj.first_name = form.cleaned_data.get("name")
        obj.last_name = form.cleaned_data.get("lastname")
        obj.username = form.cleaned_data.get("username")
        obj.email = form.cleaned_data.get("email")
        obj.save()
        return redirect(".")

    context = {
        "form" : form
    }
    return render(request,"signup.html",context)


####################################################################################

@login_required()
def private_chat_view(request, pv_id):
    form = SendMessagePVModelForm(request.POST or None)
    if form.is_valid():
        object          = form.save(commit=False)
        object.user     = request.user
        object.datetime = datetime.now()
        object.roomid_id   = pv_id
        object.unread       = True
        object.save()

    obj = Chat.objects.filter(roomid_id=pv_id).order_by('datetime')

    for i in obj:
        i.time = i.datetime.time()
        i.firstChar = i.message[0]

    cursor3 = connection.cursor()
    cursor3.execute('''Update chat_chat 
                            Set unread=0
                            WHERE   NOT (user_id = ''' + str(request.user.id) + ''')
                                    AND (roomid_id =''' + str(pv_id) + ''')''')


    form = SendMessageModelForm()

    cursor = connection.cursor()
    cursor.execute('''select chat_room.id 
                        FROM chat_room, chat_members, auth_user 
                        WHERE ((auth_user.id =''' + str(request.user.id) + ''') 
                                AND auth_user.id = chat_members.userid_id)
                                AND (chat_members.roomid_id = chat_room.id )
                                AND (chat_room.PV = 1)''')
    user_id_rooms = cursor.fetchall()   # room haye PV ke taraf tooshoone

    user_id_rooms = [i[0] for i in user_id_rooms]

    user_name_rooms = []
    unreads = []
    for id in user_id_rooms:
        cursor = connection.cursor()
        cursor.execute('''select auth_user.username
                            FROM chat_room, chat_members, auth_user 
                            WHERE (auth_user.id = chat_members.userid_id)
                                    AND (chat_members.roomid_id = chat_room.id )
                                    AND (chat_room.id = ''' + str(id) + ''')
                                    AND (chat_room.PV = 1)''')
        name_rooms = cursor.fetchall()
        # print(name_rooms)
        name1_rooms = name_rooms[0]
        name2_rooms = name_rooms[1]
        if name1_rooms[0] != request.user.username:
            # print(name1_rooms)
            # print(request.user.username)
            user_name_rooms.append(name1_rooms[0])   # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)
        else:
            # print(name2_rooms)
            user_name_rooms.append(name2_rooms[0])  # pv name kasayi ke bahashon pv dari
            # print(user_name_rooms)

        cursor2 = connection.cursor()  # Tedad Unread Ha Ro Mikhad Hesab Kone
        cursor2.execute('''select DISTINCT SUM(unread)
                                FROM (((chat_chat
                                    INNER JOIN chat_room    ON chat_chat.roomid_id = chat_room.id)
                                    INNER JOIN chat_members ON chat_members.roomid_id = chat_room.id)
                                    INNER JOIN auth_user    ON chat_members.userid_id = auth_user.id)
                                WHERE   NOT (chat_chat.user_id = ''' + str(request.user.id) + ''')
                                        AND (chat_room.id = ''' + str(id) + ''')
                                        AND (chat_chat.user_id = auth_user.id)''')
        temp_unreads = cursor2.fetchall()
        unread = temp_unreads[0]
        unread = unread[0]
        if unread == None:
            unreads.append(0)
        else:
            unreads.append(unread)  # List Az PV Ha Va Unread Hashon

    pv_list = []
    for i in range(len(user_name_rooms)):
        pv = PrivateChat(id=user_id_rooms[i], name=user_name_rooms[i], unread=unreads[i])  # har dafe ye instance az pv misaze
        pv_list.append(pv)  # ye list az PV ha
        # print(pv_list[i].id)
        # print(pv_list[i].name)

    context = {
        "pv_list": pv_list,
        "tool_2": tool_2,
        "obj": obj,
        "form": form,
        "user": request.user,
    }

    return render(request, "chat.html", context)


