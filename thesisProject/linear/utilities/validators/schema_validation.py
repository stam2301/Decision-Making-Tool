import django
from django.core.validators import BaseValidator
import jsonschema


schema = {}

class JSONSchemaValidator(BaseValidator):
	def compare(self, input, schema):
		try:
			jsonschema.validate(input.read(), schema)
		except jsonschema.exceptions.ValidationError:
			raise django.core.exceptions.ValidationError('%(value)s failed JSON schema check', params={'value': input})