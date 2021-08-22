import json, logging, os, copy

def handle_research(research, dec_root, id, nodes, edges, level):
    max_value =  -2.2250738585072014e-308 
    research_chance = dict({})

    research_chance['describe'] = copy.deepcopy(research['describe'])
    research_chance['profit/loss'] = copy.deepcopy(research['cost'])
    research_chance['decisionToChance'] = dict({})
    research_chance['decisionToChance']['leafs']=[]
    research_chance['decisionToChance']['decisions']=[]
    decisions = []
    decision = dict({})
    for research_result in research['reliability_table']:
        
        decision.clear()
    
        decision['describe'] = research_result['description']
        probability = 0
            
        i=0
        while i<(len(research['initial'])):
            probability += research['initial'][i]['chance']*research_result['forecast'][i]
            i += 1
        
        decision['probability'] = probability
        chanceToDecision = dict({})
        chanceToDecision['criterion'] = copy.deepcopy(dec_root['criterion'])
        chanceToDecision['decisions'] = copy.deepcopy(dec_root['decisions'])
        chanceToDecision['chances'] = copy.deepcopy(dec_root['chances'])
        chanceToDecision['leafs'] = copy.deepcopy(dec_root['leafs'])

        chanceToDecision['researches'] = []
        decision['chanceToDecision'] = chanceToDecision.copy()
        for dec in decision['chanceToDecision']['decisions']:
            d = dict({})
            d['describe'] = dec['describe']
            d['profit/loss'] = dec['decisionToDecision']['value']
            decision['chanceToDecision']['leafs'].append(d.copy())
        decision['chanceToDecision']['decisions'] = []
        for chan in decision['chanceToDecision']['chances']:
            for deci in chan['decisionToChance']['decisions']:
                l = dict({})
                l['describe'] = deci['describe']
                l['probability'] = deci['probability'] 
                l['chanceToLeaf'] = dict({})
                l['chanceToLeaf']['describe'] = " "
                l['chanceToLeaf']['profit/loss'] = deci['value']
                chan['decisionToChance']['leafs'].append(l.copy())
            
            j=0
            while j<(len(research['initial'])):
                chan['decisionToChance']['leafs'][j]['probability'] = round(research['initial'][j]['chance']*research_result['forecast'][j]/probability, 5)
                j += 1
        
        decisions.append(copy.deepcopy(decision)) 
    research_chance['decisionToChance']['decisions'] = decisions

    id+=1
    research_chance['decisionToChance']['id'] = id
    if (dec_root['criterion'] == 'equivalent certainty'):
        id = handle_chance_bayes(research_chance['decisionToChance'], research_chance['decisionToChance']['id'], nodes, edges, (level+1))
        
    elif (dec_root['criterion'] == 'MAXIMIN'):
        id = handle_chance_maximin(research_chance['decisionToChance'], research_chance['decisionToChance']['id'], nodes, edges, (level+1))
        
    else: 
        id = handle_chance_maximax(research_chance['decisionToChance'], research_chance['decisionToChance']['id'], nodes, edges, (level+1))
        
    if (max_value < research_chance['decisionToChance']['value'] + research_chance['profit/loss']):
        max_value = research_chance['decisionToChance']['value'] + research_chance['profit/loss']

    nodes.append(create_node(research_chance['decisionToChance']['id'], str(round(research_chance['decisionToChance']['value'], 2)), 'research', level).copy())
    edges.append(create_edge(dec_root['id'], research_chance['decisionToChance']['id'], research_chance['describe'] +" κέρδος/κόστος:" + str(research_chance['profit/loss'])))

    research_return=dict({})
    research_return['id'] = id
    research_return['chance'] = copy.deepcopy(research_chance)

    return copy.deepcopy(research_return)

def create_node(id, label, group, level):
    node = dict({})
    node['id'] = id
    node['label'] = label
    node['group'] = group
    node['level'] = level
    return node

def create_edge(fath_id, child_id, describe):
    edge = dict({})
    edge['from'] = fath_id
    edge['to'] = child_id
    edge['label'] = describe
    return edge

def handle_decision (decision_root, id, nodes, edges, level):
    max_value =  -2.2250738585072014e-308
    for decision in decision_root['decisions']:
        id+=1
        decision['decisionToDecision']['id'] = id
        id = handle_decision(decision['decisionToDecision'], decision['decisionToDecision']['id'], nodes, edges, (level+1))
        nodes.append(create_node(decision['decisionToDecision']['id'], str(round(decision['decisionToDecision']['value'], 2)), 'decision', level).copy())
        edges.append(create_edge(decision_root['id'], decision['decisionToDecision']['id'], decision['describe'] + " κέρδος/κόστος:" + str(decision['profit/loss'])))
        if (max_value < decision['decisionToDecision']['value'] + decision['profit/loss']):
            max_value = decision['decisionToDecision']['value'] + decision['profit/loss']
    
    for chance in decision_root['chances']:
        id+=1
        chance['decisionToChance']['id'] = id
        if (decision_root['criterion'] == 'equivalent certainty'):
            id = handle_chance_bayes(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges, (level+1))
        
        elif (decision_root['criterion'] == 'MAXIMIN'):
            id = handle_chance_maximin(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges, (level+1))
        
        else: 
            id = handle_chance_maximax(chance['decisionToChance'], chance['decisionToChance']['id'], nodes, edges, (level+1))
        
        if (max_value < chance['decisionToChance']['value'] + chance['profit/loss']):
            max_value = chance['decisionToChance']['value'] + chance['profit/loss']

        nodes.append(create_node(chance['decisionToChance']['id'], str(round(chance['decisionToChance']['value'], 2)), 'chance', level).copy())
        edges.append(create_edge(decision_root['id'], chance['decisionToChance']['id'], chance['describe'] + " κέρδος/κόστος:" + str(chance['profit/loss'])))

    for leaf in decision_root['leafs']:
        id+=1
        leaf['id'] = id
        nodes.append(create_node(leaf['id'], str(round(leaf['profit/loss'],2)), 'leaf', (level+1)).copy())
        edges.append(create_edge(decision_root['id'], leaf['id'], leaf['describe']).copy())
        if (max_value < leaf['profit/loss']):
            max_value = leaf['profit/loss']
    
    while((len(decision_root['researches']))>0):
        research = copy.deepcopy(decision_root['researches'][0])
        decision_root['researches'].pop(0)
        research_chance = handle_research(copy.deepcopy(research), copy.deepcopy(decision_root), id, nodes, edges, level)
        id = research_chance['id']
        decision_root['chances'].append(copy.deepcopy(research_chance['chance']))
        if(max_value < research_chance['chance']['decisionToChance']['value'] - research_chance['chance']['profit/loss']):
            max_value = research_chance['chance']['decisionToChance']['value'] - research_chance['chance']['profit/loss']

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
        if (max_value == leaf['profit/loss'] + leaf['profit/loss']):
            leaf['selected'] = True
        else:
            leaf['selected'] = False

    decision_root['value'] = max_value
    return id
        
    

def handle_chance_bayes (chance_root, id, nodes, edges, level):
    value = 0       

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges, (level+1))
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(decision['chanceToDecision']['value'],2)), 'decision', level).copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        value = value + decision['probability'] * decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(leaf['chanceToLeaf']['profit/loss'],2)), 'leaf', (level+1)).copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(round(leaf['probability']*100, 2))+chr(37)).copy())
        value = value + leaf['probability'] * leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = value
    return id

def handle_chance_maximin (chance_root, id, nodes, edges, level):
    min_value = 1.7976931348623157e+308       

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges, (level+1))
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(decision['chanceToDecision']['value'], 2)), 'decision', level).copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        if (min_value > decision['chanceToDecision']['value']):
            min_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(leaf['chanceToLeaf']['profit/loss'], 2)), 'leaf', (level+1)).copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(round(leaf['probability']*100, 2))+chr(37)).copy())
        if (min_value > leaf['chanceToLeaf']['profit/loss']):
            min_value = leaf['chanceToLeaf']['profit/loss']

    chance_root['value'] = min_value
    return id

def handle_chance_maximax (chance_root, id, nodes, edges, level):
    max_value = -2.2250738585072014e-308     

    for decision in chance_root['decisions']:
        id+=1
        decision['chanceToDecision']['id'] = id
        id = handle_decision(decision['chanceToDecision'], decision['chanceToDecision']['id'], nodes, edges, (level+1))
        nodes.append(create_node(decision['chanceToDecision']['id'], str(round(round(decision['chanceToDecision']['value'], 2), 2)), 'decision', level).copy())
        edges.append(create_edge(chance_root['id'], decision['chanceToDecision']['id'], decision['describe']+": "+str(decision['probability']*100)+chr(37)).copy())
        if (max_value < decision['chanceToDecision']['value']):
            max_value = decision['chanceToDecision']['value']
    
    for leaf in chance_root['leafs']:
        id+=1
        leaf['chanceToLeaf']['id'] = id
        nodes.append(create_node(leaf['chanceToLeaf']['id'], str(round(round(leaf['chanceToLeaf']['profit/loss'], 2),2)), 'leaf', (level+1)).copy())
        edges.append(create_edge(chance_root['id'], leaf['chanceToLeaf']['id'], leaf['describe']+": "+str(round(leaf['probability']*100, 2))+chr(37)).copy())
        if (max_value < leaf['chanceToLeaf']['profit/loss']):
            max_value = leaf['chanceToLeaf']['profit/loss']
    
    chance_root['value'] = max_value
    return id



def dectree_algo_main (input):
    vis_data = dict({})
    id = 1
    level = 0
    nodes = list([])
    edges = list([])
    
    #input file to python dict
    data = input
    root = data['headNode'] #get the head node
    root['id'] = id
    id = handle_decision(root, id, nodes, edges, (level+1))
    nodes.append(create_node(root['id'], str(round(root['value'], 2)), 'startNode', level).copy())
    vis_data['nodes'] = sorted(nodes, key=lambda x: x['id'])
    vis_data['edges'] = edges
    return vis_data