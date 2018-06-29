from django.db import models
from datetime import datetime
# Create your models here.

class EventModel(models.Model):
    id              =models.AutoField(primary_key=True)
    occur_date      =models.DateField(null=False,default=datetime.now)
    content         =models.CharField(max_length=258,null=True,)
    timestamp       =models.DateTimeField(auto_now_add=False,auto_now=True,null=True)

    def __str__(self):
        return str(self.id) 