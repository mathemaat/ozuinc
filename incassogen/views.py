from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from classes.MachtigingenCSVParser import MachtigingenCSVParser
from classes.OZUIncasso import OZUIncasso

def index(request):
    start, end = OZUIncasso.get_season()
    context = {'seizoen': 'Seizoen {}-{}'.format(start, end)}
    return render(request, 'incassogen/index.html', context)

def generate(request):
    if request.method != 'POST' or 'machtigingencsv' not in request.FILES:
        context = {'error': 'Geen bestand geüpload'}
        return render(request, 'incassogen/index.html', context)
    file = request.FILES['machtigingencsv']
    if file.content_type != 'text/csv':
        context = {'error': 'Geen geldig csv-bestand geüpload' }
        return render(request, 'incassogen/index.html', context)
    data = file.read().decode('utf-8')
    csvparser = MachtigingenCSVParser(data)
    if csvparser.is_clean():
        if csvparser.is_valid():
            now = datetime.now()
            members = csvparser.get_ozu_members()
            incasso = OZUIncasso(members)
            incasso.generate_incasso(datetime.now())
            xmlfile = open(OZUIncasso.XML_TMP_FILE, 'r')
            filename = 'incasso{}.xml'.format(now.strftime('%Y%m%d'))
            response = HttpResponse(xmlfile.read() , content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            return response
        else:
            return HttpResponse('<br />'.join(csvparser.validation_errors()))
    else:
        return HttpResponse('<br />'.join(csvparser.get_sanitisation_errors()))
