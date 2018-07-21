from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'incassogen/index.html')

def generate(request):
    if request.method != 'POST' or 'machtigingencsv' not in request.FILES:
        context = {'error': 'Geen bestand geüpload'}
        return render(request, 'incassogen/index.html', context)
    file = request.FILES['machtigingencsv']
    if file.content_type != 'text/csv':
        context = {'error': 'Geen geldig csv-bestand geüpload' }
        return render(request, 'incassogen/index.html', context)
    return render(request, 'incassogen/generate.html')
