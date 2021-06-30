import numpy as np
from fractions import Fraction
import json

from numpy.lib.function_base import insert # so that numbers are not displayed in decimal.



def simplex_main(input):
    output = dict({})
    output['iterations'] = dict({})
    simplex_array = list([])  #contains the coefficients of the constraints
    simplex_index = list([])
    b = list([])  #contains the amount of resourses
    c_base = list([])
    c_stable = list([])  #contains coefficients of objective function
    base = list([])
    n = input['number'] #πληθος μεταβλητών απόφασης
    activities_length = len(input['activities']) #πλήθος των activites
    m_coef = 100000
    iteration = 0
    
    s_length = 0
    a_length = 0

    for activity in input['activities']:
        if activity[n] == 1:
            a_length += 1
        elif activity[n] == 2:
            a_length += 1
            s_length += 1
        elif activity[n] == 3:
            s_length += 1

    c_stable = input['objective']['values']
    c_stable = c_stable + [0]*s_length
    c_stable = c_stable + [m_coef]*a_length
    c_stable = np.array(c_stable)
    
    criterion = 1
    if input['optimize'] == "minimize":
        c_stable = c_stable * (-1)
        criterion = -1


    i=1
    while i < n+1 :
        simplex_index.append("X"+str(i))
        i+=1
    i=1
    while i < s_length+1:
        simplex_index.append("S"+str(i))
        i+=1
    i=1
    while i < a_length+1:
        simplex_index.append("A"+str(i))
        i+=1
    simplex_index = np.array(simplex_index)

    i = 0
    j = 0
    sList = list([])
    aList = list([])
    for activity in input['activities']:
        s = [0]*s_length
        a = [0]*a_length
        if activity[n] == 1:
            a[j] = 1
            base.append("A"+str(j+1))
            j += 1
        elif activity[n] == 2:
            s[i] = -1
            a[j] = 1
            base.append("A"+str(j+1))
            j += 1
            i += 1
        elif activity[n] == 3:
            s[i] = 1
            base.append("S"+str(i+1))
            i += 1
        sList.append(s)
        aList.append(a)
    
    i=0
    for activity in input["activities"]:
        simplex_array.append(activity[:n])
        if len(sList)>0:
            simplex_array[i] = simplex_array[i] + sList[i]
        if len(aList)>0:
            simplex_array[i] = simplex_array[i] + aList[i]
        i += 1
        b.append(activity[n+1])

    for item in base:
        c_base.append(c_stable[np.where(simplex_index == item)[0][0]])

    c_base = np.array(c_base)
    simplex_array = np.array(simplex_array)
    b = np.array(b)
    base = np.array(base)
    z = 0
    

    reached = 0
    #iteration += 1
    unbounded = 0
    alternate = 0

    while reached == 0:
        c_dynamic = list([])
        i = 0
        while (i < c_stable.size):
            c_dynamic.append(c_stable[i] - np.sum( simplex_array[:,i] * c_base))
            i += 1
        c_dynamic = np.array(c_dynamic)
        #έλεγχος αν υπάρχει εναλλακτική λύση
        c_dyn_non_base = simplex_index
        for item in base:
            c_dyn_non_base = np.delete(c_dyn_non_base, np.where(c_dyn_non_base == item)[0][0])

        i=0
        z=0
        for item in base:
            z = z + b[i]*c_stable[np.where(simplex_index == item)[0][0]]
            i += 1
        z = z * criterion

        output['iterations'][iteration] = dict({})
        output['iterations'][iteration]['simplex_ind'] = simplex_index.tolist()
        output['iterations'][iteration]['simplex_arr'] = simplex_array.tolist()
        output['iterations'][iteration]['base'] = base.tolist()
        output['iterations'][iteration]['c_base'] = c_base.tolist()
        output['iterations'][iteration]['c_stable'] = c_stable.tolist()
        output['iterations'][iteration]['b'] = b.tolist()
        output['iterations'][iteration]['z'] = z
        output['iterations'][iteration]['relative_profit'] = c_dynamic.tolist()


        
        flag = 0
        for profit in c_dynamic:
            if profit>0:
                flag = 1
                break
        if flag == 0:
            for item in c_dyn_non_base:
                if (c_dynamic[np.where(simplex_index == item)[0][0]] == 0):
                    alternate = 1
                    break
            reached = 1
            break
        
        #διαδικασία αλλαγής βάσης
        insert = np.where(c_dynamic == max(c_dynamic))[0][0]
        
        min = m_coef
        leave = -1
        i = 0

        while i < base.size :
            if (b[i]>0 and simplex_array[i][insert]>0):
                val = b[i]/simplex_array[i][insert]
                if val < min:
                    min = val
                    leave = i
            i += 1
        
        if leave == -1:
            unbounded = 1
            break

        
        pivot_index = [int(leave), int(insert)]
        pivot = simplex_array[leave][insert]
        output['iterations'][iteration]['pivot_index'] = pivot_index
        output['iterations'][iteration]['pivot'] = float(pivot)
        #prepare for next iteration
        iteration +=1
        #divide the row of pivot with the pivot
        simplex_array[leave,:] = simplex_array[leave,:]/pivot
        b[leave] = b[leave]/pivot

        #row operation for the rest
        i=0
        while i < simplex_array.shape[0]:
            if i != leave:
                b[i] = b[i] - simplex_array[i][insert] * b[leave]
                simplex_array[i,:] = simplex_array[i,:] - simplex_array[i][insert] * simplex_array[leave, :]
                
            i += 1
        #assign new basic variable
        base[leave] = simplex_index[insert]
        c_base[leave] = c_stable[insert]
    output['unbounded'] = unbounded
    output['alternate'] = alternate
    if unbounded == 0:
        obj_variables = simplex_index[:n]
        obj_variables_in_base = []
        for item in base:
            if item in obj_variables:
                obj_variables_in_base.append(item)

        solution = dict({})
        solution['z'] = z
        solution['variables'] = [0]*n
        for item in obj_variables_in_base:
            solution['variables'][np.where(simplex_index == item)[0][0]] = float(b[np.where(base == item)[0][0]])
        output['solution'] = solution
    return output
