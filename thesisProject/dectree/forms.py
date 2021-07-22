from django import forms
from django.core.validators import FileExtensionValidator
from dectree.utilities.validators.schema_validation import JSONSchemaValidator

MY_JSON_FIELD_SCHEMA = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"definitions":{
		"startNode":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"label": {
					"type": "string",
					"enum": ["start"]},
				"group": {
					"type": "string",
					"enum": ["startNode"]},
				"criterion":{
					"type": "string",
					"enum": ["BAYES", "MAXIMIN", "MAXIMAX"]
				},
				"title":{
					"type": "string",
					"enum": ["BAYES", "MAXIMIN", "MAXIMAX"]
				}
			}
		},
		"decision":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"label": {"type": "string"},
				"group": {
					"type": "string",
					"enum": ["decision"]},
				"criterion":{
					"type": "string",
					"enum": ["BAYES", "MAXIMIN", "MAXIMAX"]
				},
				"title":{
					"type": "string",
					"enum": ["BAYES", "MAXIMIN", "MAXIMAX"]
				}
			}
		},
		"chance":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {
					"type": "string",
					"enum": ["chance"]},
				"label": {"type": "string"},
				"cost": {"type": "number"}
			}
		},
		"leaf":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {
					"type": "string",
					"enum": ["leaf"]},
				"label": {"type": "string"},
				"cost": {"type": "number"}
			}
		},
		"research":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"crowd": {"type": "integer"},
				"cost": {"type": "number"},
				"group": {
					"type": "string",
					"enum": ["research"]},
				"label": {"type": "string"},
				"chance_table": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"chance": {"type": "number"},
							"description":{"type": "string"}
						}
					}
				},
				"research_table":{
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"forecast": {
								"type": "array",
								"items": {"type": "number"}
							},
							"description": {"type": "string"}
						}
					}
				}
			}
		}
	},
	"type": "object",
	"properties":{
		"nodes": {
			"type": "array",
			"items": [
				{
					"AnyOf":[
					{"$ref": "#/definitions/startNode"},
					{"$ref": "#/definitions/decision"},
					{"$ref": "#/definitions/chance"},
					{"$ref": "#/definitions/leaf"},
					{"$ref": "#/definitions/research"},
					]
				}]
		},
		"edges": {
			"type": "array",
			"items": {
					"type": "object",
					"properties": {
						"id": {"type": "integer"},
						"to": {"type": "integer"},
						"from": {"type": "integer"},
						"label": {"type": "string"}
					},
					"required": [
						"id",
			            "to",
			            "from",
			            "label"
					]
			}
		}
	},
	"required": [
		"nodes",
		"edges"
	]
}

class upload_file_form (forms.Form):
    title = forms.CharField(label= 'Give a title', max_length= 50)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json']),])

#JSONSchemaValidator(limit_value=MY_JSON_FIELD_SCHEMA)