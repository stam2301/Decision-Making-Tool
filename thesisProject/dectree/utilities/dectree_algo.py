import json, logging, os

def create_node(id, label, shape):
    node = dict({})
    node['id'] = id
    node['label'] = label
    node['shape'] = shape
    return node

def create_edge(fath_id, child_id, describe):
    edge = dict({})
    edge['from'] = fath_id
    edge['to'] = child_id
    edge['title'] = describe
    return edge

def handle_decision (decision_root, id, nodes, edges):
    max_value =  -2.2250738585072014e-308

    for decision in decision_root['decisions']:
        id+=1
        decision['decisionToDecision']['id'] = id
        id = handle_decision(decision['decisionToDecision'], decision['decisionToDecision']['id'], nodes, edges)
        nodes.append(create_node(decision['decisionToDecision']['id'], str(round(decision['decisionToDecision']['value'], 2)), 'box').copy())
        edges.append(create_edge(decision_root['id'], decision['decisionToDecision']['id'], decision['describe']))
        if (max_value < decision['decisionToDecision']['value'] + decision['profit/loss']):
            max_value = decision['decisionToDecision']['value'] + decision['profit/loss']
    
    for chance in decision_root['chances']:
        id+=1
        chance['decisionToChance']['id'] = id
        if (decision_root['criterion'] == 'BAYES'):
            id = handle_chance_bayes(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges)
        
        elif (decision_root['criterion'] == 'MAXIMIN'):
            id = handle_chance_maximin(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges)
        
        else: 
            id = handle_chance_maximax(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges)
        
        if (max_value < chance['decisionToChance']['value'] + chance['profit/loss']):
            max_value = chance['decisionToChance']['value'] + chance['profit/loss']

        nodes.append(create_node(chance['decisionToChance']['id'], str(round(chance['decisionToChance']['value'], 2)), 'circle').copy())
        edges.append(create_edge(decision_root['id'], chance['decisionToChance']['id'], chance['describe']))

    for leaf in decision_root['leafs']:
        id+=1
        leaf['decisionToLeaf']['id'] = id
        nodes.append(create_node(leaf['decisionToLeaf']['id'], str(round(leaf['decisionToLeaf']['profit/loss'], 2)), 'dot').copy())
        edges.append(create_edge(decision_root['id'], leaf['decisionToLeaf']['id'], leaf['describe']).copy())
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
    return id
        
    

def handle_chance_bayes (chance_root, id, nodes, edges):
    value = 0       

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges)
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(decision['chanceToDecision']['value'], 2)), 'box').copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        value = value + decision['probability'] * decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(leaf['chanceToLeaf']['profit/loss'], 2)), 'dot').copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(leaf['probability']*100)+chr(37)).copy())
        value = value + leaf['probability'] * leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = value
    return id

def handle_chance_maximin (chance_root, id, nodes, edges):
    min_value = 1.7976931348623157e+308       

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges)
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(decision['chanceToDecision']['value'], 2)), 'box').copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        if (min_value > decision['chanceToDecision']['value']):
            min_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(leaf['chanceToLeaf']['profit/loss'], 2)), 'dot').copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(leaf['probability']*100)+chr(37)).copy())
        if (min_value > leaf['chanceToLeaf']['profit/loss']):
            min_value = leaf['chanceToLeaf']['profit/loss']

    chance_root['value'] = min_value
    return id

def handle_chance_maximax (chance_root, id, nodes, edges):
    max_value = -2.2250738585072014e-308     

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges)
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(decision['chanceToDecision']['value'], 2)), 'box').copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        if (max_value < decision['chanceToDecision']['value']):
            max_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(leaf['chanceToLeaf']['profit/loss'], 2)), 'dot').copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(leaf['probability']*100)+chr(37)).copy())
        if (max_value < leaf['chanceToLeaf']['profit/loss']):
            max_value = leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = max_value
    return id



def dectree_algo_main (input):
    vis_data = dict({})
    id = 1
    nodes = list([])
    edges = list([])
    #input file to python dict
    data = json.loads(input)
    root = data['headNode'] #get the head node
    
    root['id'] = id
    id = handle_decision(root, id, nodes, edges)
    nodes.append(create_node(root['id'], str(round(root['value'], 2)), 'box').copy())
    print(len(nodes))
    print("\n")
    print(len(edges))
    vis_data['nodes'] = nodes
    vis_data['edges'] = edges   
    return data