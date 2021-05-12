from django.http import HttpResponse
from django.template import Template, loader

def inicio(request):
    html = loader.get_template('index.html')
    view = html.render({}, request)
    return HttpResponse(view)

def busqueda(request):
    html = loader.get_template('busqueda.html')
    view = html.render({}, request)
    return HttpResponse(view)