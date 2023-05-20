from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'main/main.html')


def about(request):
    return render(request, 'main/about.html')


def tips(request):
    return render(request, 'main/help.html')
