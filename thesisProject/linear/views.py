from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import os, json, copy
from .forms import upload_file_form
from mainApp.models import Method
from .utilities.linear_algo import linear_prog_main

# Create your views here.
def linear_index(request):
    if request.method == 'GET':
        return render(request, 'linear/linear_index.html')

def upload_form(request):
    if request.method == 'POST':
        if 'run' in request.POST:
            print("HEY")
        elif 'manage' in request.POST:
            print("HEY")
    
    elif request.method == 'GET':
        form = upload_file_form()
        return render(request, 'linear/linear_upload.html',{'form':form})


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
        data = json.loads(request_getdata)
        outfile = linear_prog_main(data)
        if (outfile['success'] == False):
            return JsonResponse({"error": outfile['message']}, status=400)
        new_method.output_file = outfile
        new_method.save()
        return JsonResponse({"method_id": new_method.methodID}, status =200)

def results(request, method_id):
    if request.method == 'GET':
        method = Method.objects.get(methodID=method_id)
        data = method.output_file
        print("HEY")
        return render(request, 'linear/linear_results.html', context={})
    elif request.method == 'POST':
        print("HEY")
