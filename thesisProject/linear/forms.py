from django import forms
from django.core.validators import FileExtensionValidator

class upload_file_form (forms.Form):
    title = forms.CharField(label= 'Give a title', max_length= 50)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json'])])
