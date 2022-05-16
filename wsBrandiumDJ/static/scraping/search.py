#Se importan las librerías necesarias para el funcionamiento del sistema.
#bs4 necesaria para hacer el raspado de la página web.
import bs4
#Archivo de python que contiene las funciones que se realizaran a la base de datos.
from wsBrandiumDJ.static.scraping.db import postMarcasVigilancia, getMarcas
#selenium necesaria para la manipulación del navegador web.
from selenium import webdriver
#Uso de Keys para la manipulación del teclado.
from selenium.webdriver.common.keys import Keys
#Uso de WebDriverWait para definir tiempos de esperas con base a elementos de la página web.
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
#Se usa redirect para redirigir la página a otra url
from django.shortcuts import redirect
#messages sirve para crear y enviar mensajes de diveros tipos hacía una url
from django.contrib import messages

@csrf_exempt
def search(request):   
    #Variable p utilizada como contador con el propositos de pruebas.
    p = 1
    marcas = getMarcas()
    for m in marcas:
        print("id=")
        print(m[0])
        print(m[1])
        if (m[1]!=""):
            while True:
                #Se abre la página principal del sitio web.
                #Se asigna el interfaz de chrome.
                try:
                    driver = webdriver.Chrome('wsBrandiumDJ/static/scraping/chromedriver')
                except Exception as e:
                    messages.error(request, 'Es necesario actualizar la versión del chromedriver')
                    return redirect('/')
                sleep(30)
                driver.get('https://www.tmdn.org/tmview/#/tmview/results?page='+str(p)+'&pageSize=100&criteria=F&offices=MX,WO&territories=MX&basicSearch='+m[1])
                sleep(60)
                try:
                    #WebDriverWait permite interrumpir el proceso de ejecución con base a acciones especificas.
                    #Es necesario indicar como paramatetros el interfaz web y el tiempo maximo que va a esperar para que se
                    #cumpla la condición indicada.
                    WebDriverWait(driver,30).until(lambda d: d.find_element_by_tag_name("span"))
                except:
                    messages.error(request, 'No se encontro el navegador')
                    return redirect('/')
                print("página: " + str(p))
                p = p + 1
                sleep(10)
                try:
                    #execute_script permite ejecutar javascript.
                    #return document.body.innerHTML permite devolver todo el contenido incluido en el cuerpo de la página web.
                    innerHTML = driver.execute_script("return document.body.innerHTML")
                except:
                    messages.error(request, 'No se encontro el navegador')
                    return redirect('/')
                sleep(2)
                #html5lib permite analizar el contenido html
                root = bs4.BeautifulSoup(innerHTML, "html5lib")

                #Campos almacena todos los datos de cada uno de los registros resultantes.
                campos = []
                #registro almacena los valores requeridos de la busqueda resultante, tomados del vector campos.
                registro = []
                #val almacena el conjunto de registros con los valores requeridos que se almacenaran en la base de datos.
                val = []
                #find_all permite buscar todos los elmentos que coincidan con los parametros establecidos.
                #La clase rt-tr-group hace referencia a todos los registros contenidos en la tabla resultante de la busqueda realizada.
                elements = root.find_all("div", attrs={'class': 'rt-tr-group'})
                try:
                    #Se hace recorrido de todos los registros extraídos.
                    for element in elements:
                        #La clase rt-td hace referencia a todos los campos contenidos en cada uno de los registros.
                        #Se hace la busqueda sobre la variable element para extraer todos los campos de un registro uno a la vez.
                        marcas = element.find_all("div", attrs={'class': 'rt-td'})
                        #Se almacenan todos los campos de un registro
                        for marca in marcas:
                            #print("casilla del vector: " + str(cont))
                            #print(marca)
                            #cont = cont+1
                            campos.append(marca)

                        #Se valida que se tenga contenido dentro del campo del nombre 
                        if campos[3].text == '':
                            #Se guarda el registo con los campos especificos buscados
                            #campos[3] hace referencia al nombre de la marca.
                            #campos[8] hace referencia al número de solicitud.
                            #campos[8] hace referencia a la dirección URL que redirige a la página donde se detalla mas información de la marca.
                            #campos[6] hace referencia a la situación de la marca.
                            #campos[5] hace referencia a la clasificación de la marca.
                            registro.append(campos[8].span.text)
                            registro.append(m[0])
                            registro.append(campos[3].text)
                            registro.append("-".join(reversed(campos[4].p.text.split("/"))))
                            registro.append(campos[5].p.text)
                        else:
                            registro.append(campos[8].span.text)
                            registro.append(m[0])
                            registro.append(campos[3].span.text)  
                            registro.append("-".join(reversed(campos[4].p.text.split("/"))))
                            registro.append(campos[5].p.text)
                        
                        registro.append(datetime.now())
                        registro.append(datetime.now())
                        #Se almacena el registro
                        val.append(registro)
                        #Se limpian los vectorees campos y registros para repetetir el proceso con los demas registros contenidos en elements.
                        campos = []
                        registro = []
                        
                    #Se almacenan los registros en la base de datos.
                    #postMarcas es una función que se encuentra en el archivo de python db.py.
                    print(val)
                    postMarcasVigilancia(val)
                except:
                    print("No hay registros/paginas")
                    p = 1

                #Cierra el navegador
                driver.quit()

                print("p = " + str(p))
                if p == 1:
                    break;

    messages.success(request, 'Registro de las marcas completado')
    return redirect('/')

