
from rest_framework import serializers
from receiver.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Document
        fields  = ['document']