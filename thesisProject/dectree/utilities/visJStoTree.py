import json, copy

def manipulate_edges (rem_edges, from_node):
    from_edges = list([])
    del_edges = list([])
    for item in rem_edges:
        if (rem_edges[item]['from'] == from_node):
            from_edges.append(rem_edges[item].copy())
            del_edges.append(item)
    for item in del_edges:
        rem_edges.pop(item, None)
    return from_edges

def tree_construct (current_node, rem_edges, from_node, nodes):
    if nodes[from_node]['group'] == "startNode":
        
        current_node['criterion'] = nodes[from_node]['criterion']
        current_node['leafs'] = list([])
        current_node['chances'] = list([])
        current_node['decisions'] = list([])
        current_node['researches'] = list([])
        
        current_edges = manipulate_edges(rem_edges, from_node)
        for item in current_edges:
            id = item['to']
            if nodes[id]['group'] == "decision":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToDecision'] = dict({})
                tree_construct(temp['decisionToDecision'], rem_edges, id, nodes)
                current_node['decisions'].append(temp.copy())
            elif nodes[id]['group'] == "chance":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToChance'] = dict({})
                tree_construct(temp['decisionToChance'], rem_edges, id, nodes)
                current_node['chances'].append(temp.copy())
            elif nodes[id]['group'] == "leaf":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToLeaf'] = dict({})
                tree_construct(temp['decisionToLeaf'], rem_edges, item['to'], nodes)
                current_node['leafs'].append(temp.copy())
            elif nodes[id]['group'] == "research":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['cost'] = 0
                else: 
                    temp['cost'] = nodes[id]['cost']
                temp['initial'] = nodes[id]['chance_table'].copy()
                temp['reliability_table'] = nodes[id]['research_table'].copy()
                current_node['researches'].append(temp.copy())
                

    elif nodes[from_node]['group'] == "decision":
        
        current_node['criterion'] == nodes[from_node]['criterion']
        current_node['leafs'] = list([])
        current_node['chances'] = list([])
        current_node['decisions'] = list([])
        current_node['researches'] = list([])
        
        current_edges = manipulate_edges(rem_edges, from_node)
        for item in current_edges:
            id = item['to']
            if nodes[id]['group'] == "decision":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToDecision'] = dict({})
                tree_construct(temp['decisionToDecision'], rem_edges, id, nodes)
                current_node['decisions'].append(temp.copy())
            elif nodes[id]['group'] == "chance":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToChance'] = dict({})
                tree_construct(temp['decisionToChance'], rem_edges, id, nodes)
                current_node['chances'].append(temp.copy())
            elif nodes[id]['group'] == "leaf":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['profit/loss'] = 0
                else: 
                    temp['profit/loss'] = nodes[id]['cost']
                temp['decisionToLeaf'] = dict({})
                tree_construct(temp['decisionToLeaf'], rem_edges, id, nodes)
                current_node['leafs'].append(temp.copy())
            elif nodes[id]['group'] == "research":
                temp = dict({})
                temp['describe'] = item['label']
                if nodes[id]['cost'] is None:
                    temp['cost'] = 0
                else: 
                    temp['cost'] = nodes[id]['cost']
                temp['initial'] = nodes[id]['chance_table'].copy()
                temp['reliability_table'] = nodes[id]['research_table'].copy()
                current_node['researches'].append(temp.copy())


    elif nodes[from_node]['group'] == "chance":
        current_node['leafs'] = list([])
        current_node['decisions'] = list([])

        current_edges = manipulate_edges(rem_edges, from_node)
        for item in current_edges:
            id = item['to']
            if nodes[id]['group'] == "decision":
                temp = dict({})
                chance = item['label'].split(":")
                temp['describe'] = chance[1]
                temp['probability'] = float(chance[0])
                temp['decisionToDecision'] = dict({})
                tree_construct(temp['chanceToDecision'], rem_edges, id, nodes)
                current_node['decisions'].append(temp.copy())
            elif nodes[id]['group'] == "leaf":
                temp = dict({})
                chance = item['label'].split(":")
                temp['describe'] = chance[1]
                temp['probability'] = float(chance[0])
                temp['chanceToLeaf'] = dict({})
                tree_construct(temp['chanceToLeaf'], rem_edges, id, nodes)
                current_node['leafs'].append(temp.copy())
            
    elif nodes[from_node]['group'] == "leaf":
        current_node['describe'] = ""
        if nodes[from_node]['cost'] is None:
            current_node['profit/loss'] = 0
        else:
            current_node['profit/loss'] = nodes[from_node]['cost']
    

def tree_transform (input):
    vis_data = input
    nodes = dict({})
    edges = dict({})
    head = dict({})
    for item in vis_data['nodes']:
        id = item.pop('id')
        nodes[id] = item

    for item in vis_data['edges']:
        id = item.pop('id')
        edges[id] = item

    head['headNode'] = dict({})
    tree_construct(head['headNode'], edges, 1, nodes)
    return head