from django.db import models

# Create your models here.

class Method (models.Model):
    methodID = models.AutoField(primary_key=True)
    input_file = models.JSONField()
    output_file = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)