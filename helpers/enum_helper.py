from django.db.models import TextChoices

class ResponseType(TextChoices):
    SUCCESS="Success"
    FAILED="Failed"