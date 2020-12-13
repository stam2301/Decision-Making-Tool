from django import forms
from django.core.validators import FileExtensionValidator
from dectree.utilities.validators.schema_validation import JSONSchemaValidator

MY_JSON_FIELD_SCHEMA = {
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

class upload_file_form (forms.Form):
    
    title = forms.CharField(label= 'Give a title', max_length= 50)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json'])])
