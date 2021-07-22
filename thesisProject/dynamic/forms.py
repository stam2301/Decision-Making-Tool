from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import widgets


DYNAMIC_PROGRAMMING_OPTIONS = [
    ('route', 'Optimal route'),
    ('invest', 'Investment Planning'),
    ('store', 'Production and Store Planning')
]

class upload_file_form (forms.Form):
    title = forms.CharField(label= 'Give a title', max_length= 50)
    type = forms.ChoiceField(
        required= True,
        choices = DYNAMIC_PROGRAMMING_OPTIONS)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json'])])
