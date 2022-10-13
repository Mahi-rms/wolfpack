from django.db import models
import uuid
from accounts.models import User

class Uploads(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id",default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    uploaded_image=models.CharField(max_length=150, blank=True, null=True)
    thumbnail_image=models.CharField(max_length=150, blank=True, null=True)
    medium_image=models.CharField(max_length=150, blank=True, null=True)
    large_image=models.CharField(max_length=150, blank=True, null=True)
    grayscale_image=models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)