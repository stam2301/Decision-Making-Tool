schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions":{
  	"activity":{
  		"type": "array",
  		"items":{
  			"oneOf": [
  				{"type": "integer"}]
  		}
  	},
  	"additionalItems": False
  },
  "type": "object",
  "properties": {
    "number": {
      "type": "integer",
	  "minimum": 2,
      "maximum": 8
    },
    "optimize": {
      "type": "string",
      "enum": ["minimize", "maximize"]
    },
    "objective": {
      "type": "object",
      "properties": {
        "values": {
          "type": "array",
          "items": {"oneOf": [
  				{
  				"type": "number"}]
            }
          ,
          "additionalItems": False
        },
        "descriptions": {
          "type": "array",
          "items":{"oneOf": [
  				{
  				"type": "string"}]
            },
          "additionalItems": False
        }
      },
      "required": [
        "values",
        "descriptions"
      ]
    },
    "activities": {
      "type": "array",
      "items": {
      	"$ref": "#/definitions/activity"
      },
    "additionalItems": False 
    },
    "constraints":{
    	"type": "object"
    }
  },
  "required": [
    "number",
    "optimize",
    "objective",
    "activities",
    "constraints"
  ]
}