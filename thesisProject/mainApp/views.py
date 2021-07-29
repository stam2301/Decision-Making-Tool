from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import os, json, copy

def mainapp_index(request):
    if request.method == 'GET':
        return render(request, 'mainApp/mainapp_index.html')

def instructions(request):
    if request.method == 'GET':
        return render(request, 'mainApp/instructions.html')