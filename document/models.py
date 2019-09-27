from django.db import models
from django.contrib.auth import get_user_model
import hashlib
from django.core.files.storage import FileSystemStorage
User = get_user_model()


def get_file_name(instance, filename):
    return f'{instance.user.username}/{filename}'


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc = models.FileField(upload_to=get_file_name)
    md5sum = models.CharField(max_length=36, unique=True)


class SharedDocument(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    target = models.EmailField()
    zip = models.CharField(max_length=100, unique=True)
