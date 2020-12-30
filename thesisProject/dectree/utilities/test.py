def handle_research(research, dec_root):
    #max_value =  -2.2250738585072014e-308 
    
    research_chance = dict({})
    research_chance['describe'] = research['describe']
    research_chance['profit/loss'] = research['cost']
    research_chance['decisionToChance'] = dict({})
    research_chance['decisionToChance']['leafs']=[]
    research_chance['decisionToChance']['decisions']=[]
    decisions = []
    decision = dict({})
    for research_result in research['reliability table']:
        
        decision.clear()
    
        decision['describe'] = research_result['describe']
        probability = 0
            
        i=0
        while i<(len(research['initial'])):
            probability += research['initial'][i]*research_result['forecast'][i]
            i += 1
        
        decision['probability'] = probability
        keys = ['criterion', 'decisions', 'chances', 'leafs']
        chanceToDecision = {x:dec_root[x] for x in keys}
        chanceToDecision['researches'] = []
        decision['chanceToDecision'] = chanceToDecision
        
        for dec in decision['chanceToDecision']['decisions']:
            d = dict({})
            d['describe'] = dec['describe']
            d['profit/loss'] = dec['value']
            decision['chanceToDecision']['leafs'].append(d.copy())
        
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
                chan['decisionToChance']['leafs'][j]['probability'] = research['initial'][j]*research_result['forecast'][j]/probability
                j += 1
        #print(decisions)
        #print("\n")
        #print(json.dumps(decision, indent= 3))
        #print("\n")
        #print(json.dumps(research_chance, indent= 3))
        #print("\n")
        
        
    
    #research_chance['decisionToChance']['decisions'] = decisions
    #print(research_chance)
    #print(decisions)
        #print(decisions)
        #print("\n")
        decisions.append(decision.copy()) 
        print(decisions)
        #research_chance['decisionToChance']['decisions'].append(decision.copy())
        #print(research_chance['decisionToChance']['decisions'][0])
    #print(json.dumps(dec_root, indent= 3))
    #print("\n")
        #print(decisions)
    #print(json.dumps(research_chance, indent= 3))
    #print("\n")
        #print(research_chance['decisionToChance']['decisions'])
        #print("\n")
    #print(research_chance['decisionToChance']['decisions'])
           

    #if (dec_root['criterion'] == 'BAYES'):
    #    handle_chance_bayes(research_chance['decisionToChance'])
        
    #elif (dec_root['criterion'] == 'MAXIMIN'):
    #    handle_chance_maximin(research_chance['decisionToChance'])
          
    #else: 
    #    handle_chance_maximax(research_chance['decisionToChance'])

    #print(json.dumps(research_chance, indent= 3))    
    #if (max_value < research_chance['decisionToChance']['value'] + research_chance['profit/loss']):
    #    max_value = research_chance['decisionToChance']['value'] + research_chance['profit/loss']
    

    return research_chance
decision_root = dict({})
while((len(decision_root['researches']))>0):
        #print(json.dumps(decision_root, indent= 3))
        #print("\n")
        #chances
        
        #print(json.dumps(dec_root, indent= 3))
        #print("\n")
        research = decision_root['researches'][0].copy()
        decision_root['researches'].pop(0)
        
        #print(json.dumps(decision_root, indent= 3))
        #print("\n")
        research_chance = handle_research(research.copy(), decision_root.copy())
        #print(json.dumps(research_chance, indent= 3))
        #print("\n")
        #decision_root['chances'].append(research_chance)
        #print("Hi")
        #print(json.dumps(decision_root, indent= 3))
        #print("\n")