from jsonschema import validate, Draft7Validator


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
				"criterion": {"type": "string"},
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

def validate_schema(instance):
    validate(instance=instance, schema=schema)

    if Draft7Validator(schema).is_valid(instance):
        return True
    else:
        return False