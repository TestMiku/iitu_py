from django.db import models


class kcellEquipTitle(models.Model):
    title_name = models.CharField(max_length=55)
    
class kcellSubEquipName(models.Model):
    base_equipment_name = models.CharField(max_length=255, null=True)
    title_name = models.ForeignKey(kcellEquipTitle, on_delete=models.CASCADE, related_name='sub_equipment')
class kcellTransitionData(models.Model):
    transition_name = models.CharField(max_length=255)
    base_equipment_name = models.ForeignKey(kcellSubEquipName, on_delete=models.CASCADE)
    

class equipmentData(models.Model):
    set_code = models.CharField(max_length=55, null=True)
    sap = models.IntegerField()
    description = models.CharField(max_length=255)
    product_code = models.CharField(max_length=255)
    unit = models.CharField(max_length=55)
    q_ty_in_set = models.IntegerField()
    transition_name = models.ForeignKey(kcellTransitionData, on_delete=models.CASCADE)
    
    
