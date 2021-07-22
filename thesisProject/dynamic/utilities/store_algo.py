from copy import deepcopy
import numpy as np


def store_iter(output, data, periods, iter, f_route, f_min, prod_batch, store_batch, production_cost, storage_cost, start_stock, f_rem):
    output['iterations'][iter] = dict({})
    output['iterations'][iter]['s_nodes'] = list([])
    output['iterations'][iter]['x_nodes'] = list([])
    output['iterations'][iter]['table'] = list([])
    output['iterations'][iter]['f_nodes'] = list([])
    output['iterations'][iter]['x_min'] = list([]) 
    demand = data[periods-iter][0]
    cur_demand = data[periods-iter][0]
    cur_prod_cap = data[periods-iter][1]
    cur_store_cap = data[periods-iter][2]
    store = 0
    production = 0
    temp_arr = []
    while production <= cur_prod_cap:
        output['iterations'][iter]['x_nodes'].append(production)
        production = production +prod_batch
        temp_arr.append("-")
    while store <= cur_store_cap:
        output['iterations'][iter]['s_nodes'].append(store)
        store = store + store_batch
        output['iterations'][iter]['table'].append(deepcopy(temp_arr))
    j = 0
    
    while j<len(output['iterations'][iter]['s_nodes']):
        temp_min = 10000000
        i=0
        while i<len(output['iterations'][iter]['x_nodes']):
            if((output['iterations'][iter]['s_nodes'][j] + output['iterations'][iter]['x_nodes'][i]) < demand):
                i+=1
                continue
            elif ((output['iterations'][iter]['s_nodes'][j] + output['iterations'][iter]['x_nodes'][i]) >( output['iterations'][iter-1]['s_nodes'][-1] + demand)):
                i+=1
                break
            else:
                output['iterations'][iter]['table'][j][i] = (((production_cost[0]+(periods*production_cost[1]))*output['iterations'][iter]['x_nodes'][i]+production_cost[2]+(production_cost[3]*periods))+((storage_cost[0]+(periods*storage_cost[1]))*output['iterations'][iter]['s_nodes'][j]+storage_cost[2]+(storage_cost[3]*periods)))+output['iterations'][iter-1]['f_nodes'][int((output['iterations'][iter]['x_nodes'][i]+output['iterations'][iter]['s_nodes'][j]-demand)/store_batch)]
                if (output['iterations'][iter]['table'][j][i] < temp_min):
                    temp_min = deepcopy(output['iterations'][iter]['table'][j][i])
            i+=1
        i=0
        temp_x_min = []
        while i<len(output['iterations'][iter]['x_nodes']):
            if (type(output['iterations'][iter]['table'][j][i])!= str and temp_min ==output['iterations'][iter]['table'][j][i]) :
                output['iterations'][iter]['f_nodes'].append(deepcopy(output['iterations'][iter]['table'][j][i]))
                temp_x_min.append(deepcopy(output['iterations'][iter]['x_nodes'][i]))
            i+=1
        output['iterations'][iter]['x_min'].append(deepcopy(temp_x_min))
        j+=1
    if(periods - iter - 1 > 0):
        f_min = store_iter(output, data, periods, iter+1, f_route, f_min, prod_batch, store_batch, production_cost, storage_cost, start_stock, f_rem)
    elif(periods - iter - 1 == 0):
        iter = iter + 1
        output['iterations'][iter] = dict({})
        output['iterations'][iter]['s_nodes'] = list([start_stock])
        output['iterations'][iter]['x_nodes'] = list([])
        output['iterations'][iter]['table'] = list([])
        output['iterations'][iter]['f_nodes'] = list([])
        output['iterations'][iter]['x_min'] = list([])
        demand = data[periods-iter][0]
        cur_demand = data[periods-iter][0]
        cur_prod_cap = data[periods-iter][1]
        production = 0
        temp_arr = []
        temp_min = 10000000
        while production <= cur_prod_cap:
            output['iterations'][iter]['x_nodes'].append(production)
            production = production + prod_batch
            temp_arr.append("-")
        output['iterations'][iter]['table'].append(deepcopy(temp_arr))
        i = 0
        while i<len(output['iterations'][iter]['x_nodes']):
            if((output['iterations'][iter]['s_nodes'][0] + output['iterations'][iter]['x_nodes'][i]) < demand):
                i+=1
                continue
            elif ((output['iterations'][iter]['s_nodes'][0] + output['iterations'][iter]['x_nodes'][i]) >( output['iterations'][iter-1]['s_nodes'][-1] + demand)):
                i+=1
                break
            else:
                output['iterations'][iter]['table'][0][i] = (((production_cost[0]+(periods*production_cost[1]))*output['iterations'][iter]['x_nodes'][i]+production_cost[2]+(production_cost[3]*periods))+((storage_cost[0]+(periods*storage_cost[1]))*output['iterations'][iter]['s_nodes'][0]+storage_cost[2]+(storage_cost[3]*periods)))+output['iterations'][iter-1]['f_nodes'][int((output['iterations'][iter]['x_nodes'][i]+output['iterations'][iter]['s_nodes'][0]-demand)/store_batch)]
                if (output['iterations'][iter]['table'][0][i] < temp_min):
                    temp_min = deepcopy(output['iterations'][iter]['table'][0][i])
            i+=1
        i=0
        temp_x_min = []
        while i<len(output['iterations'][iter]['x_nodes']):
            if (type(output['iterations'][iter]['table'][0][i])!= str and temp_min ==output['iterations'][iter]['table'][0][i]) :
                output['iterations'][iter]['f_nodes'].append(deepcopy(output['iterations'][iter]['table'][0][i]))
                temp_x_min.append(deepcopy(output['iterations'][iter]['x_nodes'][i]))
            i+=1
        output['iterations'][iter]['x_min'].append(deepcopy(temp_x_min))
        f_min = output['iterations'][iter]['f_nodes'][0]
        for item in output['iterations'][iter]['x_min'][0]:
            f_route.append([item])
            f_rem.append(item + start_stock - demand)
        iter = iter-1
        demand = data[periods-iter][0]
    i=0
    length = len(f_route)
    while i < length:
        cur_route = f_route.pop(0)
        cur_rem = f_rem.pop(0)
        index = int(cur_rem/store_batch)
        for item in output['iterations'][iter]['x_min'][index]:
            temp_route = deepcopy(cur_route)
            temp_route.append(item)
            f_route.append(deepcopy(temp_route))
            f_rem.append(item + output['iterations'][iter]['s_nodes'][index] - demand)
        i+=1
    return f_min

def store_algo_main(input):
    output = dict({})
    f_min = 100000
    f_route = list([])
    output['solution'] = dict({})
    output['iterations'] = dict({})

    f_rem = list([])
    iteration = 1
    data = input['data']
    periods = input['options']['periods']
    prod_batch = input['options']['prod_batch']
    store_batch = input['options']['store_batch']
    storage_cost = input['options']['storage_cost']
    production_cost = input['options']['production_cost']
    start_stock = input['options']['start_stock']

    output['iterations'][iteration] = dict({})
    output['iterations'][iteration]['s_nodes'] = list([])
    output['iterations'][iteration]['x_nodes'] = list([])
    output['iterations'][iteration]['f_nodes'] = list([])
    demand = data[periods-iteration][0]
    cur_demand = data[periods-iteration][0]
    cur_prod_cap = data[periods-iteration][1]
    cur_store_cap = data[periods-iteration][2]
    i=0
    while cur_demand>=0:
        if (i*store_batch>demand):
            break
        if (cur_prod_cap+cur_store_cap<demand):
            break
        output['iterations'][iteration]['s_nodes'].append(i*store_batch)
        if (cur_demand>cur_prod_cap):
            output['iterations'][iteration]['x_nodes'].append(cur_prod_cap)
        else:
            output['iterations'][iteration]['x_nodes'].append(int(cur_demand/prod_batch)*prod_batch)
        cur_demand = cur_demand - store_batch
        output['iterations'][iteration]['f_nodes'].append(((production_cost[0]+(periods*production_cost[1]))*output['iterations'][iteration]['x_nodes'][-1]+production_cost[2]+(production_cost[3]*periods))+((storage_cost[0]+(periods*storage_cost[1]))*output['iterations'][iteration]['s_nodes'][-1]+storage_cost[2]+(storage_cost[3]*periods)))
        if(i*store_batch>cur_store_cap):
            break
        else:
            i+=1
    f_min = store_iter(output, data, periods, iteration+1, f_route, f_min, prod_batch, store_batch, production_cost, storage_cost, start_stock, f_rem)
    i=0
    length = len(f_route)
    while i < length:
        cur_route = f_route.pop(0)
        cur_rem = f_rem.pop(0)
        index = int(cur_rem/store_batch)
        temp_route = deepcopy(cur_route)
        temp_route.append(output['iterations'][iteration]['x_nodes'][index])
        f_route.append(deepcopy(temp_route))
        i+=1
    output['solution']['f_min'] = f_min
    output['solution']['routes'] = f_route
    return output