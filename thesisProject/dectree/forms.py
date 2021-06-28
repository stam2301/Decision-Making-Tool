from django import forms
from django.core.validators import FileExtensionValidator
from dectree.utilities.validators.schema_validation import JSONSchemaValidator

MY_JSON_FIELD_SCHEMA = {
	"$schema": "http://json-schema.org/draft-07/schema#"
}

class upload_file_form (forms.Form):
    title = forms.CharField(label= 'Give a title', max_length= 50)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json'])])