from .models import *
from rest_framework import serializers

class ConvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploads
        fields = "__all__"