invest_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions":{
    "period_data":{
      "type": "array",
      "items": {
        "oneOf":[{"type":"number"}]
      },
      "additionalItems": False
    }
  },
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": {"$ref":"#/definitions/period_data"},
      "additionalItems": False
    },
    "type": {
      "type": "string",
      "enum": ["invest"]
    },
    "options": {
      "type": "object",
      "properties": {
        "x": {
          "type": "integer"
        },
        "y": {
          "type": "integer"
        },
        "x_description": {
          "type": "string"
        },
        "y_description": {
          "type": "string"
        }
      },
      "required": [
        "x",
        "y",
        "x_description",
        "y_description"
      ]
    }
  },
  "required": [
    "data",
    "type",
    "options"
  ]
}

route_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "node":{
        "type": "object",
        "properties": {
            "id": {
                  "type": "integer"
                },
                "group": {
                  "type": "string",
                  "enum":["node","end","start"]
                },
                "label": {
                  "type": "string"
                }
        },
        "required": [
                "id",
                "group",
                "label"
              ]
    },
    "edge":{
        "type": "object",
        "properties": {
            "id": {
                  "type": "integer"
                },
                "to": {
                  "type": "integer"
                },
                "from": {
                  "type": "integer"
                },
                "label": {
                  "type": "string"
                }
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
  "properties": {
    "data": {
      "type": "object",
      "properties": {
        "edges": {
            "type": "array",
            "items": {"$ref":"#/definitions/edge"},
            "additionalItems": False
        },
        "nodes": {
            "type": "array",
            "items": {"$ref":"#/definitions/node"},
        "additionalItems": False
        }
      },
      "required": [
        "edges",
        "nodes"
      ]
    },
    "type": {
      "type": "string",
      "enum": ["route"]
    },
    "options": {
      "type": "object"
    }
  },
  "required": [
    "data",
    "type"
  ]
}

store_schema ={
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "period_data":{
      "type": "array",
      "items":{"oneOf": [{"type": "number"}]}
    }
  },
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": {"$ref":"#/definitions/period_data"},
      "additionalItems": False
    },
    "type": {
      "type": "string",
      "enum": ["store"]
    },
    "options": {
      "type": "object",
      "properties": {
        "periods": {
          "type": "integer"
        },
        "prod_batch": {
          "type": "integer"
        },
        "store_batch": {
          "type": "integer"
        },
        "storage_cost": {
          "type": "array",
          "items": {"type": "number"},
          "minItems": 4,
          "maxItems": 4,
          "additionalItems": False
        },
        "production_cost": {
          "type": "array",
          "items": {"type": "number"},
          "minItems": 4,
          "maxItems": 4,
          "additionalItems": False
        },
        "start_stock": {
          "type": "number"
        }
      },
      "required": [
        "periods",
        "prod_batch",
        "store_batch",
        "storage_cost",
        "production_cost",
        "start_stock"
      ]
    }
  },
  "required": [
    "data",
    "type",
    "options"
  ]
}