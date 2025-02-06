import uuid

from django.db import models


# -----------------------------------------------------------
class Province(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name
    
# -----------------------------------------------------------
class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    province = models.ForeignKey(Province, related_name='districts', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
# -----------------------------------------------------------
class Commune(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    district = models.ForeignKey(District, related_name='communes', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name