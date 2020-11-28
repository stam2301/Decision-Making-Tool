from django.db import models
# Create your models here.

class Method (models.Model):
    methodID = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, max_length=50)
    input_file = models.FileField(upload_to= 'inputs')
    output_file = models.FileField( upload_to= 'outputs')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.methodID