from rest_framework import serializers
from . import models


class GoogleSheetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoogleSheetData
        fields = ["id", "nomenclature", "account_number", "nomenclature_code"]

class AllGoogleSheetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoogleSheetData
        fields = "__all__"
    
class AccountNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoogleSheetData
        fields = ["account_number"]