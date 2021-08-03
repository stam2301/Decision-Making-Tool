from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import os, json, copy
from mainApp.models import Method
from .utilities.linear_algo import linear_prog_main
from .utilities.generate_plots import generate_plots_main
from .utilities.simplex import simplex_main
import jsonschema
from jsonschema import Draft7Validator
from jsonschema.validators import validate
from .utilities.validators.schema_validation import schema

# Create your views here.
def linear_index(request):
    if request.method == 'GET':
        return render(request, 'linear/linear_index.html')

def upload_form(request):
    if request.method == 'POST':
        if 'run' in request.POST:
            new_method = Method.objects.latest('methodID')
            return HttpResponseRedirect(reverse('linear:results', args=(new_method.methodID,)))
        elif 'manage' in request.POST:
            new_method = Method.objects.latest('methodID')
            return HttpResponseRedirect(reverse('linear:manage', args=(new_method.methodID,)))
    elif request.method == 'GET':
        return render(request, 'linear/linear_upload.html')

def manage(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.input_file
        no_constraints = data['number']
        optimize = data['optimize']
        activities_arr = data['activities']
        objective_values = data['objective']['values']
        objective_descriptions = data['objective']['descriptions']
        constraints_arr = list([])
        for key, value in data['constraints'].items():
            for item in value:
               item.insert(0, int(key))
               constraints_arr.append(item)
        title = method.title
        return render(request, 'linear/linear_manage.html', context={"optimize": optimize, "activities_arr": activities_arr, "objective_values": objective_values, "objective_descriptions": objective_descriptions, "constraints_arr": constraints_arr, "method_id": method_id, "title": title})
    
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('linear:results', args=(method_id,)))


def create_data(request):
    if request.method == 'GET':
        return render(request, 'linear/linear_create.html')
    elif request.method == 'POST':
        meth = Method.objects.latest('methodID')
        meth_id = meth.methodID
        return HttpResponseRedirect(reverse('linear:results', args=(meth_id,)))

def ajax_create_and_calculate(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = request.POST.get('data', None)
        data = json.loads(request_getdata)
        new_method = Method()
        new_method.title = data['title']
        del data['title']
        new_method.method_type = 'Linear Programming'
        new_method.input_file = copy.deepcopy(data)
        if data['number'] == 2:
            outfile = linear_prog_main(data)
            if (outfile['success'] == False):
                return JsonResponse({"error": outfile['message']}, status=400)
            new_method.output_file = outfile
        elif data['number'] > 2:
            outfile = simplex_main(data)
            new_method.output_file = outfile
        new_method.save()
        return JsonResponse({"method_id": new_method.methodID}, status =200)

def ajax_calculate(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = request.POST.get('data', None)
        data = json.loads(request_getdata)
        method = Method.objects.get(methodID=data['id'])
        del data['id']
        method.title = data['title']
        del data['title']
        method.input_file = copy.deepcopy(data)
        if data['number'] == 2:
            outfile = linear_prog_main(data)
            if (outfile['success'] == False):
                return JsonResponse({"error": outfile['message']}, status=400)
            method.output_file = outfile
        elif data['number'] > 2:
            outfile = simplex_main(data)
            method.output_file = outfile
        method.save()
        return JsonResponse({"method_id": method.methodID}, status =200)

def results(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.output_file
        if (method.input_file['number'] == 2):
            input_data = method.input_file
            plot_data = generate_plots_main(input_data, data)
            labels = plot_data['labels']
            plots = plot_data['plots']
            output = method.output_file
            del output['success']
            return render(request, 'linear/linear_results_am.html', context={"plots_data": plots, "plot_labels": labels, "axis_descriptions": input_data["objective"]["descriptions"], "output": output, "input": method.input_file, "title": method.title})
        else:
            return render(request, 'linear/linear_results.html', context={"output": method.output_file, "input": method.input_file, "title": method.title})
    elif request.method == 'POST':
        if 'new' in request.POST:
            return HttpResponseRedirect(reverse('linear:linear_index'))
        elif 'inspect' in request.POST:
            return HttpResponseRedirect(reverse('linear:manage', args=(method_id,)))

def ajax_upload_manage(request):
    if request.is_ajax and request.method == "POST":
        file = request.FILES.get("file")
        title = request.POST.get('title')
        json_input_data = file.read()
        data = json.loads(json_input_data)
        if Draft7Validator(schema).is_valid(data):
            new_method = Method()
            new_method.title = title
            new_method.input_file = copy.deepcopy(data)
            new_method.output_file = dict({})
            new_method.save()
            return JsonResponse({"method_id": new_method.methodID}, status =200)
        else:
            return JsonResponse({"error": ""}, status=400)

def ajax_upload_run(request):
    if request.is_ajax and request.method == "POST":
        file = request.FILES.get("file")
        title = request.POST.get('title')
        json_input_data = file.read()
        data = json.loads(json_input_data)
        if Draft7Validator(schema).is_valid(data):
            new_method = Method()
            new_method.title = title
            new_method.input_file = copy.deepcopy(data)
            new_method.input_file = copy.deepcopy(data)
            if data['number'] == 2:
                outfile = linear_prog_main(data)
                if (outfile['success'] == False):
                    return JsonResponse({"error": outfile['message']}, status=400)
                new_method.output_file = outfile
            elif data['number'] > 2:
                outfile = simplex_main(data)
                new_method.output_file = outfile
            new_method.save()
            return JsonResponse({"method_id": new_method.methodID}, status =200)
        else:
            return JsonResponse({"error": ""}, status=400)