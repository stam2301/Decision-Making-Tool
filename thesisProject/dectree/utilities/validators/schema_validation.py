import django
from django.core.validators import BaseValidator
import jsonschema
import json


schema = {
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
class JSONSchemaValidator(BaseValidator):
	def compare(self, value, schema):
		try:
			jsonschema.validate(value, schema)
		except jsonschema.exceptions.ValidationError:
			raise django.core.exceptions.ValidationError('%(value)s failed JSON schema check', params={'value': value})