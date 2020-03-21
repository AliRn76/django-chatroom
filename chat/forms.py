from django import forms

from .models import Chat
from .tools import tool_1




####################################################################################

class SingupForm(forms.Form):
    name = forms.CharField(label="First Name",widget=forms.TextInput(
            attrs={
                "placeholder": "Your First Name",
                "rows": "1",
                "blank": "False"
            }
        )
    )
    lastname = forms.CharField(label="Last Name", widget=forms.TextInput(
            attrs={
                "placeholder": "Your Last Name",
                "rows": "1",
                "null": "True"
            }
        )
    )
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder": "Your Username",
                "rows": "1",
            }
        )
    )
    password = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder": "Your Password",
                "rows": "1",
                "type" : "password",
            }
        )
    )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name = name.capitalize()
        return name

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname")
        lastname = lastname.capitalize()
        return lastname


####################################################################################

class EditProfileForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder": "Your Name",
                "rows": "1",
                "blank": "False"
            }
        )
    )
    lastname = forms.CharField(label="Last Name", widget=forms.TextInput(
            attrs={
                "placeholder": "Your Last Name",
                "rows": "1",
                "null": "True"
            }
        )
    )
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder": "Your Name",
                "rows": "1",
            }
        )
    )

    email = forms.EmailField(widget=forms.EmailInput(
            attrs={
                "placeholder": "Your Email",
                "rows": "1",
            }
        )
    )
    def clean_name(self):
        name = self.cleaned_data.get("name")
        name = name.capitalize()
        return name

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname")
        lastname = lastname.capitalize()
        return lastname

####################################################################################

class SendMessageModelForm(forms.ModelForm):
    message = forms.CharField(label='', required=False, widget=forms.Textarea(
            attrs={
                "placeholder": "Type your message",
                "rows" : "1",
                "dir" : "rtl",
                "id" : "textarea",
            }
        )
    )
    image = forms.ImageField(label='', required=False)

    class Meta:
        model = Chat
        fields = [
            'message',
            'image',
        ]

    def clean_message(self):
        message = self.cleaned_data.get("message")
        message_tmp = message.lower()
        msg = message_tmp.split()

        for i in range(len(msg)):
            if msg[i] in tool_1.Curse:
                msg[i] = "****"

        message = ' '.join(msg)

        return message


####################################################################################

class SendMessagePVModelForm(forms.ModelForm):
    message = forms.CharField(label='', required=False, widget=forms.Textarea(
            attrs={
                "placeholder": "Type your message",
                "rows" : "1",
                "dir" : "rtl",
                "id": "textarea",
            }
        )
    )

    image = forms.ImageField(label='', required=False)

    class Meta:
        model = Chat
        fields = [
            'message',
            'image',
        ]


####################################################################################

class EditMessageModelForm(forms.ModelForm):
    message = forms.CharField(label='', required=False, widget=forms.Textarea(
            attrs={
                "rows": "1",
                "placeholder": "Type your message",
                "dir": "rtl",
            }
        )
    )
    class Meta:
        model = Chat
        fields = [
            'message',
        ]

    def clean_message(self):
        message = self.cleaned_data.get("message")
        message_tmp = message.lower()

        msg = message_tmp.split()

        for i in range(len(msg)):
            if msg[i] in tool_1.Curse:
                msg[i] = "****"

        message = ' '.join(msg)

        return message
