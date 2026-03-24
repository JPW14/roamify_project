from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return render(request, 'roamify/index.html',)

def post(request):
    return render(request, 'roamify/post.html')

def destination(request):
    return render(request, 'roamify/destination.html')
