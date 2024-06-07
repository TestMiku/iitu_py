from rest_framework import serializers

from reporter import models


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ["responsible", "process", "created_at", "text"]

class processSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ['process', 'created_at']