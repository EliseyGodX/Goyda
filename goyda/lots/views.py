from django.shortcuts import render

def general(request):
    context = {'test': 123}
    return render(request, 'lots/general.html', context)

def purchases(request):
    return render