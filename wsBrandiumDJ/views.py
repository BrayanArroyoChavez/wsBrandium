from django.http import HttpResponse
from django.template import Template, loader
#Archivo de python que contiene las funciones que se realizaran a la base de datos.
from wsBrandiumDJ.static.scraping.db import getCantComp

def inicio(request):
    registros = getCantComp()
    print(registros)
    html = loader.get_template('index.html')
    view = html.render({'registros':registros}, request)
    return HttpResponse(view)

def carga(request):
    html = loader.get_template('carga.html')
    view = html.render({}, request)
    return HttpResponse(view)

def busqueda(request):
    html = loader.get_template('busqueda.html')
    view = html.render({}, request)
    return HttpResponse(view)