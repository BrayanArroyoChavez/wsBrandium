#Archivo de python que contiene la conexión a la base de datos.
from wsBrandiumDJ.static.scraping.connection import mydb

#Extrae la cantida de registros que faltan por completar
def getCantComp():
    mycursor = mydb.cursor()

    sql = "SELECT COUNT(id) as cantidad FROM `marcas_renovacions` WHERE band_completo=0"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    return result

#Extrae la fecha de registro mas reciente
def getFRR():
    mycursor = mydb.cursor()

    sql = "SELECT MAX(fecha_registro) FROM `marcas_renovacions`"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    return result

#Extrae la fecha de solicitud mas reciente
def getFSR():
    mycursor = mydb.cursor()

    sql = "SELECT MAX(fecha_solicitud) FROM `marcas_renovacions`"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    return result

#Extrae la fecha de registro mas antigua
def getFRA():
    mycursor = mydb.cursor()

    sql = "SELECT MIN(fecha_registro) FROM `marcas_renovacions` WHERE `fecha_registro` != '0000-00-00'"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    return result

#Extrae la fecha de solicitud mas antigua
def getFSA():
    mycursor = mydb.cursor()

    sql = "SELECT MIN(fecha_solicitud) FROM `marcas_renovacions` WHERE `fecha_solicitud` != '0000-00-00'"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    return result

#Inserta en la base de datos los datos de la marca resultantes de la primera etapa del raspado de la página web
def postMarcas(val):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO marcas_renovacions (nombre_marca, no_solicitud, detalles_url,situacion_marca,clasificacion_niza,createdAt,updatedAt ) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

    mycursor.executemany(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

#Extrae todas las direcciones URL almacenadas de los registros que detallan la información de las marcas
def getEnlaces():
    mycursor = mydb.cursor()

    sql = "SELECT id,detalles_url FROM `marcas_renovacions` WHERE band_completo=0"

    mycursor.execute(sql)

    result = mycursor.fetchall()

    return result

#Inserta en la base de datos los datos de la marca resultantes de la segunda etapa del raspado de la página web
def postMarcasCompletas(update):
    mycursor = mydb.cursor()
    
    sql = "UPDATE marcas_renovacions SET no_registro = %s, tipo_dpi = %s, tipo_marca = %s, clase_marca = %s, " \
    "producto_servicio = %s, fecha_solicitud = %s, fecha_registro = %s, fecha_vencimiento = %s, " \
    "nombre_solicitante = %s, municipio_solicitante = %s, direccion_solicitante = %s, pais_solicitante = %s, " \
    "telefono_solicitante = %s, correo_solicitante =%s, cp_solicitante = %s, nombre_representante = %s, " \
    "direccion_representante = %s, ciudad_representante = %s, telefono_representante = %s, correo_representante = %s, " \
    "cp_representante = %s, pais_representante = %s, imagen_url = %s, band_completo = 1 WHERE id = %s"

    val =(update[1], update[2], update[3], update[4], update[5],update[6],update[7],update[8],update[9],update[10],update[11],update[12],update[13]
    ,update[14],update[15],update[16],update[17],update[18],update[19],update[20],update[21],update[22],update[23],update[0])

    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

#Extraer nombre de las marcas para hacer busquedas con el proposito de vigilancia
def getMarcas():
    mycursor = mydb.cursor()

    sql = "SELECT id, nombre FROM `marca` where id > 77"

    mycursor.execute(sql)

    result = mycursor.fetchall()

    return result

#Inserta en la base de datos los datos de la marca vigilancia
def postMarcasVigilancia(val):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO marcas_busquedas_guardadas (no_solicitud, id_marca, nombre_marca, fecha_solicitud, clasificacion_niza,createdAt,updatedAt ) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s)" 

    mycursor.executemany(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")