from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

def generate_plots_main(input, output):
    color_codes = ["rgb(222, 49, 99, 0.5)", "rgb(204, 204, 255, 0.5)", "rgb(255, 127, 80, 0.5)", "rgb(100, 149, 237, 0.5)", "rgb(255, 191, 0, 0.5)", "rgb(64, 224, 208, 0.5)", "rgb(223, 255, 0, 0.5)", "rgb(159, 226, 191, 0.5)", "rgb(242, 79, 226, 0.5)", "rgb(46, 204, 113, 0.5)"]
    data = input
    activities = input['activities']
    constraints = input['constraints']
    
    plots = list([])
    
    c_bnd = list([])
    labels = list([])
    solution = output['values'][0]
    plot = dict({})
    plot["data"] = list([])
    plot["data"].append({
        "x": output['values'][0],
        "y": output['values'][1]
    })
    plot["label"] = "Optimal Solution"
    plot["backgroundColor"] = "rgb(0, 0, 0)"
    plot["borderColor"] = "rgb(0, 0, 0)"
    plot["radius"] = 4
    plots.append(plot)
    
    for i in range(-10, 11):
        labels.append(round(solution+(i*(solution/10)), 2))
        
    x_bnd = np.linspace(0, 2*solution, 100)
    


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
        c_bnd.append(t)
    
    min_y = 1.7976931348623157e+308 
    max_y = -2.2250738585072014e-308
    for activity in activities:
        plot = dict({})
        plot["data"] = list([])
        for item in x_bnd.tolist():
            plot["data"].append({
                "x": item,
                "y": (activity[3]/activity[1])-item*(activity[0]/activity[1])
            })
        plot["label"] = str(activity[0]) + "X1 + " +str(activity[1]) + "X2 = " + str(activity[3])
        plot["backgroundColor"] = color_codes.pop(0)
        plot["borderColor"] = plot["backgroundColor"]
        if(activity[2] == 2):
            plot["fill"] = "start"
        elif(activity[2] == 3):
            plot["fill"] = "end"
        
        plots.append(plot)

        if(((activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])) < ((activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1]))):
            if(((activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])) < min_y):
                min_y = (activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])
            if(((activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1])) > max_y):
                max_y = (activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1])
        elif(((activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])) > ((activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1]))):
            if(((activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])) > max_y):
                max_y = (activity[3]/activity[1])-(solution+((-11)*(solution/10)))*(activity[0]/activity[1])
            if(((activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1])) < min_y):
                min_y = (activity[3]/activity[1])-11*solution+(i*(11/10))*(activity[0]/activity[1])

    
    out = dict({})
    out['labels'] = labels
    out['plots'] = plots
    return out
    #for key in plots:
    #    print(activities[key])

        
    