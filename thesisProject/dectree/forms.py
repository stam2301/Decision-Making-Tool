from django import forms
from django.core.validators import FileExtensionValidator
from dectree.utilities.validators.schema_validation import JSONSchemaValidator

MY_JSON_FIELD_SCHEMA = {
	"$schema": "http://json-schema.org/draft-07/schema#",

	"definitions": {
		"startNode":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {"type": "string",
					"enum": ["startNode"]},
				"label": {"type": "string",
					"enum": ["start"]}
			},
			"required": ["id", "level", "group", "label"]
		},
		"decisionNode":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {"type": "string",
					"enum": ["decision"]},
				"label": {"type": "string"}	
			},
			"required": ["id", "level", "group", "label"]
		},
		"chance":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {"type": "string",
					"enum": ["chance"]},
				"label": {"type": "string",
					"enum": ["BAYES", "MAXIMIN", "MAXIMAX"]},
				"title": {"type": "string"}
			},
			"required": ["id", "level", "group", "label", "title"]
		},
		"leaf":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"level": {"type": "integer"},
				"group": {"type": "string",
					"enum": ["leaf"]},
				"label": {"type": "string"}
			},
			"required": ["id", "level", "group", "label"]
		},
		"research":{
			"type": "object",
			"properties": {
				"id":{"type": "integer"},
				"level": {"type": "integer"},
				"group": {"type": "string",
					"enum": ["research"]},
				"label": {"type": "string"},
				"crowd": {"type": "integer"}
			},
			"required": ["id", "level", "group", "label", "crowd"]
		},
		"edge":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"from": {"type": "integer"},
				"to": {"type": "integer"},
				"label": {"type": "string"}
			},
			"required": ["id", "from", "to"]
		},
		"chanceEdge":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"from": {"type": "integer"},
				"to": {"type": "integer"},
				"label": {"type": "string",
					"pattern": "^((U+0030)-(U+002E)-[0-9]{3})"}
			},
			"required": ["id", "from", "to", "label"]
		},
		"researchEdge":{
			"type": "object",
			"properties": {
				"id": {"type": "integer"},
				"from": {"type": "integer"},
				"to": {"type": "integer"},
				"label": {"type": "string"},
				"situation_table": {"type": "array",
					"items": {"type": "object",
						"properties": {
							"description": {"type": "string"},
							"situation": {"type": "number"}
						},
						"required": ["description", "situation"]}},
				"research_table": {"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"description": {"type": "string"},
							"forecast": {"type": "array",
								"items": {"type": "number"}}
						},
						"required": ["forecast"]
					}}
			},
			"required": ["id", "from", "to", "situation_table", "research_table"]
		}
	},
	"nodes":{
		"type": "array",
		"items": {
			"AnyOf": [
				{"$ref": "#/definitions/startNode"},
				{"$ref": "#/definitions/decision"},
				{"$ref": "#/definitions/chance"},
				{"$ref": "#/definitions/leaf"},
				{"$ref": "#/definitions/research"}]
			}
	},
	"edges": {
		"type": "array",
		"items": {
			"AnyOf": [
				{"$ref": "#/definitions/edge"},
				{"$ref": "#/definitions/chanceEdge"},
				{"$ref": "#/definitions/researchEdge"}]
		}
	}
}

class upload_file_form (forms.Form):
    
    title = forms.CharField(label= 'Give a title', max_length= 50)
    upload_file = forms.FileField(label= 'Choose file', validators=[  FileExtensionValidator(allowed_extensions=['json'])])