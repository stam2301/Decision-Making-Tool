import json, logging, os
from .schema_validation import validate_schema

def dectree_algo_main (input_file):
    data = json.loads(input_file)
    if validate_schema(data):
        print('correct schema')
    else:
        print('wrong schema')