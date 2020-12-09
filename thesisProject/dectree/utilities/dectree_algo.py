import json, logging, os
from .schema_validation import validate_schema

def handle_decision (decision_root):
    max_value =  -2.2250738585072014e-308

    for decision in decision_root['decisions']:
        handle_decision(decision['decisionToDecision'])
        if (max_value < decision['decisionToDecision']['value'] + decision['profit/loss']):
            max_value = decision['decisionToDecision']['value'] + decision['profit/loss']
    
    for chance in decision_root['chances']:
        if (decision_root['criterion'] == 'BAYES'):
            handle_chance_bayes(chance['decisionToChance'])
        
        elif (decision_root['criterion'] == 'MAXIMIN'):
            handle_chance_maximin(chance['decisionToChance'])
        
        else: 
            handle_chance_maximax(chance['decisionToChance'])
        
        if (max_value < chance['decisionToChance']['value'] + chance['profit/loss']):
            max_value = chance['decisionToChance']['value'] + chance['profit/loss']
    
    for leaf in decision_root['leafs']:
        if (max_value < leaf['decisionToLeaf']['profit/loss'] + leaf['profit/loss']):
            max_value = leaf['decisionToLeaf']['profit/loss'] + leaf['profit/loss']
    
    for decision in decision_root['decisions']:
        if (max_value == decision['decisionToDecision']['value'] + decision['profit/loss']):
            decision['selected'] = True
        else:
            decision['selected'] = False
    
    for chance in decision_root['chances']:
        if (max_value == chance['decisionToChance']['value'] + chance['profit/loss']):
            chance['selected'] = True
        else:
            chance['selected'] = False
    
    for leaf in decision_root['leafs']:
        if (max_value == leaf['decisionToLeaf']['profit/loss'] + leaf['profit/loss']):
            leaf['selected'] = True
        else:
            leaf['selected'] = False

    decision_root['value'] = max_value
        
    

def handle_chance_bayes (chance_root):
    value = 0       

    for decision in chance_root['decisions']:
        handle_decision(decision['chanceToDecision'])
        value = value + decision['probability'] * decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        value = value + leaf['probability'] * leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = value

def handle_chance_maximin (chance_root):
    min_value = 1.7976931348623157e+308       

    for decision in chance_root['decisions']:
        handle_decision(decision['chanceToDecision'])
        if (min_value > decision['chanceToDecision']['value']):
            min_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        if (min_value > leaf['chanceToLeaf']['profit/loss']):
            min_value = leaf['chanceToLeaf']['profit/loss']

    chance_root['value'] = min_value

def handle_chance_maximax (chance_root):
    max_value = -2.2250738585072014e-308     

    for decision in chance_root['decisions']:
        handle_decision(decision['chanceToDecision'])
        if (max_value < decision['chanceToDecision']['value']):
            max_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        if (max_value < leaf['chanceToLeaf']['profit/loss']):
            max_value = leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = max_value



def dectree_algo_main (input_file):
    
    #input file to python dict
    data = json.loads(input_file)
    if validate_schema(data):
        root = data['headNode'] #get the head node
        handle_decision(root)
        print(root)

    else:
        print('wrong schema')