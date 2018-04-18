from django.shortcuts import render

def index(request, string):
    return render(request, 'index.html', {})