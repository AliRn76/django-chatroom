from django import forms
from receiver.models import Document

class DocumentForm(forms.ModelForm):
    document = forms.FileField(label="")
    class Meta:
        model = Document
        fields = ('document', )