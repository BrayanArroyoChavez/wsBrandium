#mysql.connector proporciona acceso a la base de datos de mysql
import mysql.connector

#Archivo de conexión a la base de datos
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="brandium"
)