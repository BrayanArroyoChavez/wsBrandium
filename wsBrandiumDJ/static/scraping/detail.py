#Se importan las librerías necesarias para el funcionamiento del sistema.
#bs4 necesaria para hacer el raspado de la página web.
import bs4
#Archivo de python que contiene las funciones que se realizaran a la base de datos.
from wsBrandiumDJ.static.scraping.db import getEnlaces, postMarcasCompletas
#Archivo de python que contiene las funciones que se realizaran para el raspado de la página web.
from wsBrandiumDJ.static.scraping import fd
#selenium necesaria para la manipulación del navegador web.
from selenium import webdriver
#Uso de Keys para la manipulación del teclado.
from selenium.webdriver.common.keys import Keys
#Uso de WebDriverWait para definir tiempos de esperas con base a elementos de la página web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from fake_useragent import UserAgent
from time import sleep
#Se usa redirect para redirigir la página a otra url
from django.shortcuts import redirect
#messages sirve para crear y enviar mensajes de diveros tipos hacía una url
from django.contrib import messages


def detail(request):
    chrome_options = webdriver.ChromeOptions()
    #Argumentos adicionales para el interfaz de navegación con chrome
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("lang=es")

    #Se asigna el interfaz de chrome con los argumentos definidos.
    #En caso de que falle se redirige a la página de inicio y muestra el mensaje de error en pantalla
    try:
        driver = webdriver.Chrome('wsBrandiumDJ/static/scraping/chromedriver',chrome_options=chrome_options)
    except Exception as e:
        messages.error(request, 'Es necesario actualizar la versión del chromedriver')
        return redirect('/inicio/')
    #Se indica el tamaño y la posición de la ventana del navegador.
    driver.set_window_size(800,800)
    driver.set_window_position(0,0)

    #Función para obtener las direcciones URL que muestran informaciónn a detalle de las marcas.
    #getEnlaces() es una función contenida en el archivo de python db.py.
    enlaces = getEnlaces()
    print(len(enlaces))
    if len(enlaces) == 0:
        messages.error(request, 'No hay registros que completar')
        return redirect('/inicio/')
    registro = 0
    ban = 0

    #Se recorre la lista de direcciones URL
    for enlace in enlaces:
        #ua = UserAgent().random
        #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua})
        #print(driver.execute_script("return navigator.userAgent;"))

        condition = True
        #update almacena los datos faltantes de cada uno de los registros de la base de datos.
        #Se genera un vector finito de 24 campos para posicionar en lugares especificos los datos obtenidos y 
        #poder tener mayor control sobre la insersión en la base de datos
        update = ['']*24
        try:
            #Se abre la página con la dirección obtenida de la base de datos
            driver.get("https://www.tmdn.org/tmview/"+enlace[1])
        except:
            messages.error(request, 'No se encontro el navegador')
            return redirect('/inicio/')
        try:
            #WebDriverWait permite interrumpir el proceso de ejecución con base a acciones especificas.
            #Es necesario indicar como paramatetros el interfaz web y el tiempo maximo que va a esperar para que se
            #cumpla la condición indicada.
            WebDriverWait(driver,90).until(EC.presence_of_element_located((By.XPATH, "//*[@class='sc-AxiKw iIIwSC']")))
        except:
            #En caso de que no se encuentre el elemento indicado se asigna False a la variable condition para evitar 
            #realizar el proceso de raspado e intente abrir la siguiente dirección URL de la lista de enlaces
            condition = False
            ban += 1

        sleep(13)

        if (ban == 3):
            driver.quit()
            messages.success(request, 'Error al cargar las marcas')
            return redirect('/inicio/')

        if condition:
            ban = 0
            if registro == 0:
                sleep(90)
            registro += 1
            print('Registro: ' + str(registro) + ' ID:' + str(enlace[0]))

            #execute_script permite ejecutar javascript.
            #return document.body.innerHTML permite devolver todo el contenido incluido en el cuerpo de la página web.
            try:
                innerHTML = driver.execute_script("return document.body.innerHTML")
            except:
                messages.error(request, 'No se encontro el navegador')
                return redirect('/inicio/')
            sleep(2)
            #html5lib permite analizar el contenido html
            root = bs4.BeautifulSoup(innerHTML, "html5lib")

            #Se almacena en el vector el id obtenido de la base de datos
            update[0]=enlace[0]
            #Se almacena los datos de la empresa la función getEmpresa se encuentra en el archivo fd.py
            update = fd.getEmpresa(root,update)
            #Se almacena los servicios y/o productos de la empresa la función getServicio se encuentra en el archivo fd.py
            update = fd.getServicio(root,update)
            #Se almacena las fechas de solicitud, registro y vencimiento de la empresa la función getFecha se encuentra en el archivo fd.py
            update = fd.getFecha(root,update)
            #Se almacena los datos del titualar de la empresa la función getSolicitante se encuentra en el archivo fd.py
            update = fd.getSolicitante(root,update)
            #Se almacena los datos del representante la empresa la función getRepresentante se encuentra en el archivo fd.py
            update = fd.getRepresentante(root,update)

            #Se actualiza el registro en la base de datos la función postMarcasCompletas se encuentra en el archivo db.py
            postMarcasCompletas(update)
            print(update)
            update = ['']*24

    #Cierra el navegador
    driver.quit()
    messages.success(request, 'Registro de las marcas completado')
    return redirect('/inicio/')
    