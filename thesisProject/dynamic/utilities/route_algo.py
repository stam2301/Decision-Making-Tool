import copy
import numpy as np



def route_iter(cur_nodes, iter, nodes, edges, output_data, f_min, f_route, level_nodes):
    f_min_new = list([])
    output_data[iter] = dict({})
    current_nodes = list([])
    s_nodes = list([])
    temp_arr = list([])
    min_points = list([])
    for item in cur_nodes:
        for edge in edges:
            if edge['to'] == item:
                if edge['from'] in s_nodes:
                    continue
                else:
                    s_nodes.append(edge['from'])
                    level_nodes[edge['from']] = iter + 1
    temp_arr = [ [ "-" for i in range(len(cur_nodes)) ] for j in range(len(s_nodes)) ]
    j=0
    while j<len(s_nodes):
        min = 1000000
        min_point = list([])
        i=0
        while i<len(cur_nodes):
            k = len(edges)-1
            while k!=-1:
                if edges[k]['to'] == cur_nodes[i] and edges[k]['from'] == s_nodes[j]:
                    temp_arr[j][i] = f_min[i] + int(edges[k]['label'])
                    if temp_arr[j][i] < min:
                        min = temp_arr[j][i]
                    edges.remove(edges[k])
                    k-=1
                else:
                    k-=1
            i+=1
        f_min_new.append(min)
        i=0
        while i<len(cur_nodes):
            if min == temp_arr[j][i]:
                min_point.append(cur_nodes[i])
            i+=1
        min_points.append(min_point)
        j+=1
    output_data[iter]['table'] = temp_arr
    output_data[iter]['cur_nodes'] = cur_nodes
    output_data[iter]['s_nodes'] = s_nodes
    output_data[iter]['min_points'] = min_points
    output_data[iter]['f_min'] = f_min_new
    if len(edges)!=0:
        f_min = route_iter(s_nodes, iter+1, nodes, edges, output_data, f_min_new, f_route, level_nodes)
    if len(f_route) == 0:
        temp_min = 100000
        i=0
        for item in f_min_new:
            if item < temp_min:
                temp_min = item
        for item in f_min_new:
            if item == temp_min:
                i+=1
        j=0
        f_min = temp_min
        temp_index = 0
        while j < i:
            index = f_min_new.index(temp_min, temp_index)
            temp_start = s_nodes[index]
            for item in min_points[index]:
                f_route.append([temp_start, item])
            temp_index = index+1
            j+=1
    else:
        i = 0
        length = len(f_route)
        while i < length:
            cur_route = f_route.pop(0)
            index = s_nodes.index(cur_route[-1])
            for item in min_points[index]:
                temp_route = copy.deepcopy(cur_route)
                temp_route.append(item)
                f_route.append(temp_route)

            i+=1
    return f_min


def route_algo_main(input):
    level_nodes = dict({})
    data = copy.deepcopy(input)
    output = dict({})
    f_min = 0
    output_data = dict({})
    f_route = []
    output['solution'] = dict({})
    output['iterations'] = dict({})
    nodes = dict({})
    current_nodes = list([])
    iteration = 1
    edges = data['data']['edges']
    for node in input['data']['nodes']:
        nodes[node['id']] = node['group']
        if node['group'] == 'end':
            current_nodes.append(node['id'])
            level_nodes[node['id']] = iteration
    output_data[iteration] = dict({})
    output_data[iteration]['s'] = list([])
    output_data[iteration]['f_min'] = list([])
    output_data[iteration]['x_min'] = list([])
    output_data[iteration]['cur_nodes'] = current_nodes
    cur_nodes = list([])
    for item in current_nodes:
        i = len(edges)-1
        while i!=-1:
            if edges[i]['to'] == item:
                output_data[iteration]['x_min'].append(edges[i]['to'])
                output_data[iteration]['f_min'].append(int(edges[i]['label']))
                output_data[iteration]['s'].append(edges[i]['from'])
                cur_nodes.append(edges[i]['from'])
                level_nodes[edges[i]['from']] = iteration + 1
                edges.remove(edges[i])
                i-=1
            else:
                i-=1
    f_min_array = output_data[iteration]['f_min']
    f_min = route_iter(cur_nodes, iteration+1, nodes, edges, output_data, f_min_array, f_route, level_nodes)
    i = 0
    length = len(f_route)
    while i < length:
        cur_route = f_route.pop(0)
        index = output_data[iteration]['s'].index(cur_route[-1])
        cur_route.append( output_data[iteration]['x_min'][index])
        f_route.append(cur_route)
        i+=1
    output['solution']['f_min'] = f_min
    output['solution']['routes'] = f_route
    output['iterations'] = output_data
    for item in data['data']['nodes']:
        item['level'] = level_nodes[item['id']]
    
    output['input'] = data['data']
    output['input']['edges'] = copy.deepcopy(input['data']['edges'])
    return output