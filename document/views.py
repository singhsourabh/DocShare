from django.shortcuts import render, redirect
from .models import Document, SharedDocument
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import DocumentCreateSerializer, DocumentSerializer, SharedDocumentSerializer
from rest_framework import mixins
import hashlib
from io import BytesIO
import os
import zipfile
from django.core.files.storage import default_storage
import uuid


class DocumentList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DeleteDocument(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DoucumentUpload(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentCreateSerializer

    def post(self, request, *args, **kwargs):
        for f in request.data.getlist('documents'):
            serializer = self.serializer_class
            md5 = hashlib.md5()
            for chunk in f.chunks():
                md5.update(chunk)
            md5sum = md5.hexdigest()
            s = serializer(data={'user': self.request.user.pk,
                                 'doc': f, 'md5sum': md5sum})
            if s.is_valid():
                s.save()
        return Response({'details': 'successfully created'}, status=HTTP_200_OK)


class DocumentShare(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id_list = request.data.getlist('shared_doc')
        target = request.data.get('target')
        qs = Document.objects.filter(Q(pk__in=id_list) & Q(user=request.user))
        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in qs:
                zf.write(f.doc.path)
        file_name = default_storage.save("%s.zip" % (uuid.uuid4()), mem_zip)
        SharedDocument.objects.create(
            user=request.user, target=target, zip=file_name)
        return Response({'details': 'successfully shared'}, status=HTTP_200_OK)


class ShareList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SharedDocument.objects.filter(target=self.request.user.email)
    serializer_class = SharedDocumentSerializer
