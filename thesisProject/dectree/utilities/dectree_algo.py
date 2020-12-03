import json, logging, os


def dectree_algo_main (input_file):
    
    data = json.load(input_file)
    print("Done reading")
    print(data)