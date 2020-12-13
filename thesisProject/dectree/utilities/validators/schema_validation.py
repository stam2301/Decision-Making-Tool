import django
from django.core.validators import BaseValidator
import jsonschema


schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",

	"definitions": {
		"leaf":{
			"type": "object",
			"properties": {
				"describe":{"type": "string"},
				"profit/loss": {"type": "number"}
			}
		},

		"chance":{
			"type": "object",
			"properties": {
				"leafs": {
					"type": "array",
					"items":{
						"type": "object",
						"properties": {
							"describe":{"type": "string"},
							"probability": {"type": "number"},
							"chanceToLeaf": {"$ref": "#/definitions/leaf"}
						}
					}
				},
				"decisions": {
					"type": "array",
					"items":{
						"type": "object",
						"properties":{
							"describe":{"type": "string"},
							"probability": {"type": "number"},
							"chanceToDecision": {"$ref": "#/definitions/decision"}
						}
					}
				}
			}
		},

		"decision":{
			"type": "object",
			"properties": {
				"criterion": {  "type": "string",
                                "enum": ["BAYES", "MAXIMIN", "MAXIMAX"]},
				"leafs": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"describe":{"type": "string"},
							"profit/loss": {"type": "number"},
							"decisionToLeaf": {"$ref": "#/definitions/leaf"}
						}
					}
				},
				"chances": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"describe": {"type": "string"},
							"profit/lost": {"type": "number"},
							"decisionToChance": {"$ref": "#/definitions/chance"}
						}
					}
				},
				"decisions": {
					"type": "array",
					"items":{
						"type": "object",
						"properties":{
							"describe":{"type": "string"},
							"probability": {"type": "number"},
							"DecisionToDecision": {"$ref": "#/definitions/decision"}
						}
					}
				}
			}
		}


	},
	"type": "object",
	"properties":{
		"headNode": {"$ref": "#/definitions/decision"}
	}
}

class JSONSchemaValidator(BaseValidator):
	def compare(self, input, schema):
		try:
			jsonschema.validate(input.read(), schema)
		except jsonschema.exceptions.ValidationError:
			raise django.core.exceptions.ValidationError('%(value)s failed JSON schema check', params={'value': input})