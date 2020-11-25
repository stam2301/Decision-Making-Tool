from django import forms

class upload_file_form (forms.Form):
    title = forms.CharField(label="Give a title", max_length=50)
    selected_file = forms.FileField()