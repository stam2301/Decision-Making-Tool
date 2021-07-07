import numpy as np



def invest_iter(iter, f_prev, x, y, data_table, output, f_route, f_max):
    output['iterations'][iter] = dict({})
    if iter == y:
        max_points = []
        max_point = 0
        i = 0
        temp_arr = []
        while i <= x:
            temp_arr.append(f_prev[x-i] + data_table[y-iter][i])
            if temp_arr[i]>= max_point:
                max_point = temp_arr[i]
            i+=1
        i = 0
        while i <= x:
            if temp_arr[i] == max_point:
                max_points.append(i)
                f_route.append([i])
            i += 1
        f_max = max_point
        output['iterations'][iter]['table'] = temp_arr
        output['iterations'][iter]['f_max'] = f_max
        output['iterations'][iter]['x_max'] = max_points
        return f_max

    else: 
        temp_arr = []
        f_cur = []
        max_points = []
        i = 0
        while i<=x:
            j = 0
            max_point = []
            max = -1
            temp = [0] * (x+1)
            while True:
                temp[j] = f_prev[i-j] + data_table[y-iter][j]
                if(temp[j] >= max):
                    max = temp[j]
                if i == j:
                    j = 0
                    while j <= i:
                        if temp[j] == max:
                            max_point.append(j)
                        j += 1
                    f_cur.append(max)
                    break
                j += 1
            temp_arr.append(temp)
            max_points.append(max_point)
            i += 1
        output['iterations'][iter]['table'] = temp_arr
        output['iterations'][iter]['f_max'] = f_cur
        output['iterations'][iter]['x_max'] = max_points
        f_max = invest_iter(iter+1,f_cur, x, y, data_table, output, f_route, f_max)
        i = 0
        length = len(f_route)
        while i < length:
            cur_route = f_route.pop(0)
            for item in max_points[x-sum(cur_route)]:
                cur_route.append(item)
                f_route.append(cur_route)
            i += 1
        return f_max


        

    

def invest_algo_main(input):
    data = input

    f_max = 0
    f_route = []
    output = dict({})
    output['solution'] = dict({})
    output['iterations'] = dict({})

    data_table = input['data']
    x = input['options']['x']
    y = input['options']['y']
    n = 1
    i = 0
    f_last = input['data'][y-1]
    
    output['iterations']['1'] = dict({})
    output['iterations']['1']['f_max'] = f_last
    output['iterations']['1']['x_max'] = list([])
    while i<=x:
        output['iterations']['1']['x_max'].append(i)
        i+=1
    f_max = invest_iter(n+1, f_last, x, y, data_table, output, f_route, f_max)
    i = 0
    length = len(f_route)
    while i < length:
        cur_route = f_route.pop(0)
        cur_route.append(f_last[x-sum(cur_route)])
        f_route.append(cur_route)
        i += 1
    output['solution']['f_max'] = f_max
    output['solution']['routes'] = f_route
    return output