# serializers.py
from rest_framework import serializers

from main.models import AvhUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvhUser
        fields = '__all__'
