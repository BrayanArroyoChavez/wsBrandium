#Se importan las librerías necesarias para el funcionamiento del sistema.
#bs4 necesaria para hacer el raspado de la página web.
import bs4
#Archivo de python que contiene las funciones que se realizaran a la base de datos.
from wsBrandiumDJ.static.scraping.db import postMarcas
#selenium necesaria para la manipulación del navegador web.
from selenium import webdriver
#Uso de Keys para la manipulación del teclado.
from selenium.webdriver.common.keys import Keys
#Uso de WebDriverWait para definir tiempos de esperas con base a elementos de la página web.
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def scraping(request):   
    fecharegistro = request.POST.get('fStart') + " - " + request.POST.get('fEnd')
    print(fecharegistro)
    #Variable p utilizada como contador con el propositos de pruebas.
    p = 1
    #Se asigna el interfaz de chrome.
    driver = webdriver.Chrome('wsBrandiumDJ/static/scraping/chromedriver.exe')
    #Se abre la página principal del sitio web.
    driver.get('https://www.tmdn.org/tmview/#/tmview')
    sleep(30)
    #find_element_by_xpath permite buscar etiquetas con atributos en especificos (Arroja el primer elemento encontrado)
    #el atributo debe de estar dentre de corchetes [] y el contenido se debe concatenar con un @ al inicio.
    #Se busca la etiqueta button que contenga los atributos definidos y se hace click.
    #el botón despliega las opciones avanzadas de busqueda.
    driver.find_element_by_xpath("//button[@data-test-id='advanced-search']").click()
    sleep(10)
    #ActionChains permite las interaciones con el teclado y los movimientos y acciones con el mouse.
    #move_to_element mueve el mouse hacia el elemento indicado.
    #send_keys envia la cadena de caracteres al elemento seleccionado.
    #Se selecciona el campo que permite definir el territorio en los parametros de busqueda.
    #Dado que el campo es un elemento al que no se le puede hacer focus fue necesario hacer la selección del elemento mediante las funciones indicadas.
    webdriver.ActionChains(driver).move_to_element(driver.find_element_by_xpath("//div[@class='Select-input']")).click(driver.find_element_by_xpath("//div[@class='Select-input']")).send_keys("MX").perform()
    sleep(10)
    #send_keys en este caso envia la función de la tecla enter.
    #Dado que el campo de territorios despliega una lista de selccion 
    #se usa Enter para seleccionar la opcione resultante provinientes de la indicación anterior realizada.
    driver.find_element_by_xpath("//div[@class='Select-input']/input").send_keys(Keys.ENTER)
    #find_elements_by_xpath permite buscar etiquetas con atributos en especificos(Arroja todos los elementos que coincidan con las características definidas).
    driver.find_elements_by_xpath("//input[@class='datepicker-textfield']")[1].send_keys("01/05/2011 - 30/05/2011")
    driver.find_element_by_xpath("//button[@data-test-id='search-button']").click()
    #current_url extrae la dirección URL actual en la que esta posicionado el navegador.
    #Se remplaza en la URL la cantidad de registros que se mostraran por página.
    driver.get(driver.current_url.replace('pageSize=30', 'pageSize=100'))

    condition = True
    while condition: 
        #WebDriverWait permite interrumpir el proceso de ejecución con base a acciones especificas.
        #Es necesario indicar como paramatetros el interfaz web y el tiempo maximo que va a esperar para que se
        #cumpla la condición indicada.
        WebDriverWait(driver,30).until(lambda d: d.find_element_by_tag_name("span"))
        print("página: " + str(p))
        sleep(10)
        #execute_script permite ejecutar javascript.
        #return document.body.innerHTML permite devolver todo el contenido incluido en el cuerpo de la página web.
        innerHTML = driver.execute_script("return document.body.innerHTML")
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
                registro.append(campos[3].text)
                registro.append(campos[8].span.text)
                registro.append(campos[8].a['href'])
                registro.append(campos[6].text)
                registro.append(campos[5].p.text)
            else:
                registro.append(campos[3].span.text)
                registro.append(campos[8].span.text)
                registro.append(campos[8].a['href'])
                registro.append(campos[6].text)
                registro.append(campos[5].p.text)
            
            registro.append(datetime.now())
            registro.append(datetime.now())
            print(registro)
            #Se almacena el registro
            val.append(registro)
            #Se limpian los vectorees campos y registros para repetetir el proceso con los demas registros contenidos en elements.
            campos = []
            registro = []
            
        #Se almacenan los registros en la base de datos.
        #postMarcas es una función que se encuentra en el archivo de python db.py.
        postMarcas(val)

        try:
            #Permite avanzar en la siguiente página de busqueda.
            #Dado que en la primera página de busqueda los elementos de navegación estan deshabilitados 
            #la indicacion definida trera el elemento requerido como primer resultado por lo que se indica 
            #que se debe seleccionar el elemento [0] a diferencia de las siguientes página donde ya se habilitan 
            #las opciones de volver a la primera página o anterior, el elemento de página siguiente estara situado 
            #en la posición [2] del vector resultante.
            if p == 1:
                driver.find_elements_by_xpath("//a[@class='sc-fznyYp fRaeqU sc-fznBtT kPhgXf']")[0].click()
            else:
                driver.find_elements_by_xpath("//a[@class='sc-fznyYp fRaeqU sc-fznBtT kPhgXf']")[2].click()
            p = p + 1
        except:
            #En caso de que no pueda seleccionar el elemento indicado indicara que ya no hay elementos siguientes 
            #por lo que el proceso se considera como terminado y se asinga a la variables condition el valor de False
            #para romper con el ciclo While
            condition = False
    
    #Cierra el navegador
    driver.quit()
