from django.shortcuts import render, redirect
from .forms import upload_file_form
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

# Create your views here.
def dectree_index(request):
    if request.method == 'GET':
        return render(request, 'dectree/decision_tree_index.html')

def upload_form(request):

    if request.method == 'POST':
        if 'run' in request.POST:
            input_form = upload_file_form(request.POST, request.FILES)
            #print (input_form)
            if input_form.is_valid():
                new_method = input_form.save(commit=False)
                #print (new_method)
                #print (request.FILES)
                new_method.input_file = request.FILES['input_file']
                new_method.output_file = request.FILES['input_file']
                new_method.save()
                #print (new_method.input_file)
                
            return redirect('/dectree/results/')
        
        elif 'manage' in request.POST:
            return redirect('/dectree/manage/')
        
    elif request.method == 'GET':
        form = upload_file_form()
        return render(request, 'dectree/decision_tree_upload.html',{'form':form})


def show_results(request):
    if request.method == 'GET':
        return render(request, 'dectree/decision_tree_results.html')

def manage_tree(request):
    if request.method == 'GET':
        return render(request, 'dectree/decision_tree_manage.html')