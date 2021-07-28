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
            },
            "required": ["id", "level", "label", "group", "criterion", "title"]
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
            },
            "required": ["id", "level", "label", "group", "criterion", "title"]
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
            },
            "required": ["id", "level", "label", "group", "cost"]
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
            },
            "required": ["id", "level", "label", "group", "cost"]
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
            },
            "required": ["id", "level", "crowd", "cost", "chance_table", "research_table", "label", "group"]
        },
        "edge":{
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
    },
    "type": "object",
    "properties":{
        "nodes": {
            "type": "array",
            "items":{
                "oneOf": [
                    {"$ref": "#/definitions/startNode"},
                    {"$ref": "#/definitions/decision"},
                    {"$ref": "#/definitions/chance"},
                    {"$ref": "#/definitions/leaf"},
                    {"$ref": "#/definitions/research"},
                ]
                },
            "additionalItems": False
        },
        "edges": {
            "type": "array",
            "items": [
                    {"$ref": "#/definitions/edge"}
            ]
        }
    },
    "required": [
        "nodes",
        "edges"
    ]
}