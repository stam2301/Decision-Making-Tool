from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import os, json, copy
from mainApp.models import Method
from .forms import upload_file_form
from .utilities.store_algo import store_algo_main
from .utilities.production_algo import production_algo_main
from .utilities.invest_algo import invest_algo_main


def dynamic_index(request):
    if request.method == 'GET':
        return render(request, 'dynamic/dynamic_index.html')

def upload_form(request):
    if request.method == 'POST':
        if 'run' in request.POST:
            input_form = upload_file_form(request.POST, request.FILES)
            if input_form.is_valid():
                if request.POST.get('type') == 'route':
                    print("HEY")
                    return render(request, 'linear/linear_upload.html',{'form':input_form})
                elif request.POST.get('type') == 'invest':
                    return render(request, 'linear/linear_upload.html',{'form':input_form})
                elif request.POST.get('type') == 'production':
                    return render(request, 'linear/linear_upload.html',{'form':input_form})
            else:
                return render(request, 'linear/linear_upload.html',{'form':input_form})

        elif 'manage' in request.POST:
            input_form = upload_file_form(request.POST, request.FILES)
            if input_form.is_valid():
                new_method = Method()
                new_method.title = request.POST.get('title')
                new_method.method_type = 'Dynamic Programming'
                json_file = request.FILES['upload_file']
                json_input_data = json_file.read()
                new_method.input_file = json.loads(json_input_data)
                new_method.output_file = dict({})
                new_method.save()
            else:
                return render(request, 'linear/linear_upload.html',{'form':input_form})
            return HttpResponseRedirect(reverse('dynamic:manage', args=(new_method.methodID,)))
    
    elif request.method == 'GET':
        form = upload_file_form()
        return render(request, 'dynamic/dynamic_upload.html',{'form':form})

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
        print(data)
        new_method = Method()
        new_method.title = data['title']
        del data['title']
        new_method.method_type = "Dynamic Programming"
        new_method.input_file = copy.deepcopy(data)
        if data['type'] == "store":
            outfile = store_algo_main(data)
            print("store")
        elif data['type'] == "invest":
            outfile = invest_algo_main(data)
        elif data['type'] == "production":
            outfile = production_algo_main(data)
            print("production")
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
        if data['type'] == "store":
            outfile = store_algo_main(data)
            print("store")
        elif data['type'] == "invest":
            outfile = invest_algo_main(data)
        elif data['type'] == "production":
            outfile = production_algo_main(data)
            print("production")
        method.output_file = outfile
        method.save()
        return JsonResponse({"method_id": method.methodID}, status =200)

def results(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        input = method.input_file
        output = method.output_file
        if input['type'] == "invest":
            return render(request, 'dynamic/dynamic_results_invest.html', context={"input": input, "output": output})
    elif request.method == 'POST':
        if 'new' in request.POST:
            return HttpResponseRedirect(reverse('dynamic:dynamic_index'))
        elif 'inspect' in request.POST:
            return HttpResponseRedirect(reverse('dynamic:manage', args=(method_id,)))