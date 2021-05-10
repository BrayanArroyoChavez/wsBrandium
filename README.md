<h1>Instrucciones</h1>

<h2>Instalaciones necesarias:</h2>
<p>pip install beautifulsoup4</p>
<p>pip install selenium</p>
<p>pip install html5lib</p>
<p>pip install mysql-connector-python</p>
<p>pip install django-heroku</p>
<p>pip install mysql-connector-python</p>
<p>pip install gunicorn</p>


<h2>Descripción de archivos:</h2>
<p>main.py - Archivo que se encarga de realizar la primera parte del web scraping, en el cual se hace la busqueda
especifica de la información y se realiza el recorrido de páginas del resultado obtenido para almacenar la 
información resultante en la base de datos.</p>
<p>detail.py - Archivo que se encarga de realizar la segunda parte del web scraping, en el cual se accede 
directamente a la dirección URL obtenida del proceso en el archivo main.py, para raspar la información detalla 
sobre las marcas.</p>
<p>fd.py - Archivo directamente ligado a detail.py en el cual se contienen las funciones que se encargan de realizar
el raspado especifico a la página web.</p>
<p>connection.py - Archivo de conexión a la base de datos.</p>
<p>db.py - Archivo que almance las funciones a la base de datos que son requeridas en los archivos main.py y detail.py</p>

<h2>Nota:</h2>
<p>EL archivo chromedriver.exe es utilizado por selenium y debe estar al mismo nivel que los archivos main.py y detail.py para su correcto funcionamiento.</p>
<p>La versión del archivo chromedriver.exe debe de coincidir con la versión actual del nevageador de chrome que tenga el SO.</p>

<h2>Prueba en linea</h2>
<p>Para probar el código en línea ingrese al siguiente enlace</p>
<a href=https://wsbrandium.herokuapp.com/inicio/>Prueba</a>