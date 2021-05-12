import json, copy



def find_researches(data):
    #data = json.loads(input)
    researches = dict({})
    #print(data)
    for item in data['nodes']:
        if item['group'] == "research":
            researches[item['id']] = dict({})
            researches[item['id']]['research_table'] = item['research_table']
            researches[item['id']]['chance_table'] = item['chance_table']
    return researches
