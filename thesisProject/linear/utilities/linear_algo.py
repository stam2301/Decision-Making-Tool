from numpy import true_divide
from scipy.optimize import linprog
import numpy as np





def linear_prog_main(input):

    print(input)
    print("\n")
    data = input
    n = int(data['number'])
    
    lhs_ineq = list([])
    rhs_ineq = list([])

    lhs_eq = list([])
    rhs_eq = list([])

    bnd = list([])
    
    output = dict({})

    if (data['optimize'] == "maximize"):
        obj = [(-1)*x for x in data['objective']['values']]
    else:
        obj = data['objective']['values']
    
    for activity in data['activities']:
        if (activity[n] == 2):
            for x in range(0, n):
                activity[x] = activity[x]*(-1)
            
            activity[n] = 3
            activity[n+1] = activity[n+1]*(-1)
        if (activity[n] == 3):
            rhs_ineq.append(activity.pop(n+1))
            activity.pop(n)
            lhs_ineq.append(activity)
        elif (activity[n] == 1):
            rhs_eq.append(activity.pop(n+1))
            activity.pop(n)
            lhs_eq.append(activity)

    for key in data['constraints']:
        min = -2.2250738585072014e-308
        max = 1.7976931348623157e+308
        equal = -2.2250738585072014e-308
        temp = ()
        for item in data['constraints'][key]:
            if (item[0] == 2):
                if(min<item[1]):
                    min = item[1]
            elif (item[0]==3):
                if(max>item[1]):
                    max = item[1]
            elif(item[0] == 1):
                max = item[1]
                min = item[1]
        
        if(max<min):
            output['success'] = False
            output['message'] = "Your constraints are overlapping!"
            return output

        t = (min, max)
        bnd.append(t)
        
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd, method="revised simplex")

    output['success'] = opt.success
    output['message'] = opt.message
    output['values'] = (opt.x).tolist()
    output['names'] = data['objective']['descriptions']
    return output