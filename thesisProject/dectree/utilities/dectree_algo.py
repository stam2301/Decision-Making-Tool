import json, logging, os
from django.templatetags.static import static

input_dir = 'inputs/'

def read_json (file_dir):
    try:
        print('Reading from input')
        with open(static(file_dir), 'r') as f:
            return json.load(f)
    finally:
        print('Done reading')

def dectree_algo_main (input_file_name):
    input_file_dir = os.path.join(input_dir,input_file_name)
    return_dict = read_json(input_file_dir)
    print(return_dict)