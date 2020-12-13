from django.db import models
# Create your models here.

class Method (models.Model):
    methodID = models.AutoField(primary_key=True)
    method_type = models.CharField(blank= True, max_length=50)
    title = models.CharField(blank=True, max_length=50)
    input_file = models.JSONField()
    output_file = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.methodID