from django.http import HttpResponse
from django.template import Template, loader
#Archivo de python que contiene las funciones que se realizaran a la base de datos.
from wsBrandiumDJ.static.scraping.db import getCantComp, getFSR, getFRR
import locale

# Idioma "es-ES" (código para el español de España)
locale.setlocale(locale.LC_ALL, 'es-ES') 

def inicio(request):
    registros = getCantComp()
    print(registros)
    html = loader.get_template('index.html')
    view = html.render({'registros':registros}, request)
    return HttpResponse(view)

def carga_detalle(request):
    html = loader.get_template('carga_detalle.html')
    view = html.render({}, request)
    return HttpResponse(view)

def carga_main(request):
    html = loader.get_template('carga_main.html')
    view = html.render({}, request)
    return HttpResponse(view)

def busqueda(request):
    fsr = getFSR()
    fsr = fsr[0].strftime("%d de %B del %Y")
    print(fsr)
    frr = getFRR()
    frr = frr[0].strftime("%d de %B del %Y")
    print(frr)
    html = loader.get_template('busqueda.html')
    view = html.render({'fsr': fsr, 'frr': frr}, request)
    return HttpResponse(view)