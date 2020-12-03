from django import forms
from mainApp.models import Method

class upload_file_form (forms.ModelForm):
    class Meta:
        model = Method
        fields = ('title','input_file')