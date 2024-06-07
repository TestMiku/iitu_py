from rest_framework import serializers
from . import models

class allDataByEquip(serializers.ModelSerializer):
    class Meta:
        model = models.kcellTransitionData
        fields = "__all__"

class allSubDataByEquip(serializers.ModelSerializer):
    class Meta:
        model = models.equipmentData
        fields = ['id', 'set_code', 'sap', 'description', 'product_code', 'unit', 'q_ty_in_set']