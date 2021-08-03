from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import os, json, copy
from mainApp.models import Method
from .utilities.store_algo import store_algo_main
from .utilities.invest_algo import invest_algo_main
from .utilities.route_algo import route_algo_main
import jsonschema
from jsonschema import Draft7Validator
from jsonschema.validators import validate
from .utilities.validators.schema_validation import route_schema, invest_schema, store_schema

def dynamic_index(request):
    if request.method == 'GET':
        return render(request, 'dynamic/dynamic_index.html')

def upload_form(request):
    if request.method == 'POST':
        if 'run' in request.POST:
            new_method = Method.objects.latest('methodID')
            return HttpResponseRedirect(reverse('dynamic:results', args=(new_method.methodID,)))
        
        elif 'manage' in request.POST:
            new_method = Method.objects.latest('methodID')
            return HttpResponseRedirect(reverse('dynamic:manage', args=(new_method.methodID,)))
    
    elif request.method == 'GET':
        #form = upload_file_form()
        return render(request, 'dynamic/dynamic_upload.html')

def manage(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.input_file
        return render(request, 'dynamic/dynamic_manage.html', context={"method_id" :method_id ,"input_title": method.title, "input_type": data['type'], "input_options": data['options'], "input_data": data['data']})
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('dynamic:results', args=(method_id,)))

def create_data(request):
    if request.method == 'GET':
        return render(request, 'dynamic/dynamic_create.html')
    elif request.method == 'POST':
        meth = Method.objects.latest('methodID')
        meth_id = meth.methodID
        return HttpResponseRedirect(reverse('dynamic:results', args=(meth_id,)))

def ajax_create_and_calculate(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = request.POST.get('data', None)
        data = json.loads(request_getdata)
        new_method = Method()
        new_method.title = data['title']
        del data['title']
        new_method.method_type = "Dynamic Programming"
        new_method.input_file = copy.deepcopy(data)
        if data['type'] == "route":
            new_method.input_file['options'] = dict({})
        if data['type'] == "store":
            outfile = store_algo_main(data)
        elif data['type'] == "invest":
            outfile = invest_algo_main(data)
        elif data['type'] == "route":
            outfile = route_algo_main(data)
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
        if data['type'] == "route":
            method.input_file['options'] = dict({})
        if data['type'] == "store":
            outfile = store_algo_main(data)
        elif data['type'] == "invest":
            outfile = invest_algo_main(data)
        elif data['type'] == "route":
            outfile = route_algo_main(data)
        method.output_file = outfile
        method.save()
        return JsonResponse({"method_id": method.methodID}, status =200)

def results(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        input = method.input_file
        output = method.output_file
        if input['type'] == "invest":
            return render(request, 'dynamic/dynamic_results_invest.html', context={"input": input, "output": output, "title":method.title})
        elif input['type'] == "route":
            return render(request, 'dynamic/dynamic_results_route.html', context={"input": input, "output": output, "title":method.title})
        elif input['type'] == "store":
            return render(request, 'dynamic/dynamic_results_store.html', context={"input": input, "output": output, "title":method.title})
    elif request.method == 'POST':
        if 'new' in request.POST:
            return HttpResponseRedirect(reverse('dynamic:dynamic_index'))
        elif 'inspect' in request.POST:
            return HttpResponseRedirect(reverse('dynamic:manage', args=(method_id,)))

def ajax_upload_manage(request):
    if request.is_ajax and request.method == "POST":
        file = request.FILES.get("file")
        title = request.POST.get('title')
        type = request.POST.get('type')
        json_input_data = file.read()
        data = json.loads(json_input_data)
        if type == "route":
            if Draft7Validator(route_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = dict({})
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)
        elif type == "invest":
            if Draft7Validator(invest_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = dict({})
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)    
        elif type == "store":
            if Draft7Validator(store_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = dict({})
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)
        else:
            return JsonResponse({"error": ""}, status=400)
    else:
            return JsonResponse({"error": ""}, status=400)

def ajax_upload_run(request):
    if request.is_ajax and request.method == "POST":
        file = request.FILES.get("file")
        title = request.POST.get('title')
        type = request.POST.get('type')
        json_input_data = file.read()
        data = json.loads(json_input_data)
        if type == "route":
            if Draft7Validator(route_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                data['options'] = dict({})
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = route_algo_main(data)
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)
        elif type == "invest":
            if Draft7Validator(invest_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = invest_algo_main(data)
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)    
        elif type == "store":
            if Draft7Validator(store_schema).is_valid(data):
                new_method = Method()
                new_method.title = title
                new_method.input_file = copy.deepcopy(data)
                new_method.output_file = store_algo_main(data)
                new_method.save()
                return JsonResponse({"method_id": new_method.methodID}, status =200)
        else:
            return JsonResponse({"error": ""}, status=400)
    else:
            return JsonResponse({"error": ""}, status=400)