from django.shortcuts import render
from .forms import upload_file_form

# Create your views here.

def upload_form(request):
    form = upload_file_form()

    if request.method == 'POST':
        form = upload_file_form(request.POST)

        #if form.is_valid():

        #if 'inspect_tree' in request.POST:

        #Selif 'run_method' in request.POST:


    return render(request, 'dectree/decision_tree_upload.html',{'form':form})