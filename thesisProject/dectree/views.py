from django.shortcuts import render, redirect
from jsonschema.validators import validate
from .forms import upload_file_form
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from .utilities.dectree_algo import dectree_algo_main
from .utilities.find import find_researches
from .utilities.visJStoTree import tree_transform
import os, json, copy
from mainApp.models import Method


# Create your views here
def dectree_index(request):
    if request.method == 'GET':
        return render(request, 'dectree/decision_tree_index.html')

def upload_form(request):

    if request.method == 'POST':
        if 'run' in request.POST:
            input_form = upload_file_form(request.POST, request.FILES)
            
            if input_form.is_valid():
                new_method = Method()
                new_method.title = request.POST.get('title')
                new_method.method_type = 'Decision Tree'
                json_file = request.FILES['upload_file']
                json_input_data = json_file.read()
                data = json.loads(json_input_data)
                tree_data = tree_transform(data)
                new_method.output_file = dectree_algo_main(tree_data)
                new_method.input_file = json.loads(json_input_data)
                new_method.save()
            else: 
                return render(request, 'dectree/decision_tree_upload.html',{'form':input_form})

            return HttpResponseRedirect(reverse('dectree:results', args=(new_method.methodID,)))
        
        elif 'manage' in request.POST:
            input_form = upload_file_form(request.POST, request.FILES)
            if input_form.is_valid():
                new_method = Method()
                new_method.title = request.POST.get('title')
                new_method.method_type = 'Decision Tree'
                json_file = request.FILES['upload_file']
                json_input_data = json_file.read()
                new_method.input_file = json.loads(json_input_data)
                new_method.output_file = dict({})
                new_method.save()
            else:
                return render(request, 'dectree/decision_tree_upload.html',{'form':input_form})
            return HttpResponseRedirect(reverse('dectree:manage', args=(new_method.methodID,)))

    elif request.method == 'GET':
        form = upload_file_form()
        return render(request, 'dectree/decision_tree_upload.html',{'form':form})


def results(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.output_file
        db_edges = data['edges']
        db_nodes = data['nodes']
        return render(request, 'dectree/decision_tree_results.html', context={"db_nodes": db_nodes, "db_edges":db_edges})
    elif request.method == 'POST':
        if 'new' in request.POST:
            return HttpResponseRedirect(reverse('dectree:dectree_index'))
        elif 'inspect' in request.POST:
            return HttpResponseRedirect(reverse('dectree:manage', args=(method_id,)))


def manage(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.input_file
        researches = find_researches(data)
        nodes = data['nodes']
        edges = data['edges']
        nodes_id = len(nodes)
        edges_id = len(edges)
        title = method.title
        return render(request, 'dectree/decision_tree_manage.html', context={"nodes": nodes, "edges": edges, "title": title, "edges_id": edges_id, "nodes_id": nodes_id, "researches": researches, "method_id": method_id})
    
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('dectree:results', args=(method_id,)))

def create_tree(request):
    if request.method == 'GET':
        return render(request, 'dectree/decision_tree_create.html')
    if request.method == 'POST':
        meth = Method.objects.latest('methodID')
        meth_id = meth.methodID
        return HttpResponseRedirect(reverse('dectree:results', args=(meth_id,)))

def ajax_calculate(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = request.POST.get('data', None)
        data = json.loads(request_getdata)
        method = Method.objects.get(methodID=data['id'])
        del data['id']
        method.title = data['title']
        del data['title']
        method.input_file = copy.deepcopy(data)
        tree = tree_transform(data)
        method.output_file = dectree_algo_main(tree)
        method.save()
        return JsonResponse({"method_id": method.methodID}, status =200)

def ajax_create_and_calculate(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = request.POST.get('data', None)
        data = json.loads(request_getdata)
        new_method = Method()
        new_method.title = data['title']
        del data['title'] 
        new_method.method_type = 'Decision Tree'
        new_method.input_file = copy.deepcopy(data)
        data = json.loads(request_getdata)
        tree = tree_transform(data)
        new_method.output_file = dectree_algo_main(tree)
        new_method.save()
        return JsonResponse({"method_id": new_method.methodID}, status =200)