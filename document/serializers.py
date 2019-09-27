from docshare.settings import MEDIA_ROOT
from rest_framework import serializers
from .models import Document, SharedDocument
from django.core.files.storage import FileSystemStorage
import hashlib


class DocumentSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField('get_filename')

    class Meta:
        model = Document
        fields = ['id', 'document', 'md5sum', 'doc']

    def get_filename(self, obj):
        return obj.doc.name.split('/', 1)[-1]


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['user', 'doc', 'md5sum']


class SharedDocumentSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    zip_file = serializers.SerializerMethodField('get_file')

    class Meta:
        model = SharedDocument
        fields = ['owner', 'zip_file']

    def get_owner(self, obj):
        return obj.user.username

    def get_file(self, obj):
        return self.context.get('request').build_absolute_uri(FileSystemStorage(location=MEDIA_ROOT).url(obj.zip))
