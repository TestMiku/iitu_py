from rest_framework import serializers
from . import models


class ExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExcelData
        fields = ["id", "name", "document_number"]

class AllExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExcelData
        fields = "__all__"
    
class NamesExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExcelData
        fields = ["name"]
        
class ProjectExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExcelData
        fields = ["project"]
        
class ProjectManagerExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExcelData
        fields = ["project_manager"]