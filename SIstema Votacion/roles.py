import psycopg2
import random
conexion1 = psycopg2.connect(user = "postgres",
                                 password = "12345678",
                                  host = "localhost",
                                  port = "8081",
                                  database = "sistema_votacion")

cursor1=conexion1.cursor()
sql="insert into roles(idroles, roles_descripcion) values (%s,%s)"
datos=(1, "administrador")
cursor1.execute(sql, datos)


cursor2=conexion1.cursor()
sql="insert into roles(idroles, roles_descripcion) values (%s,%s)"
datos=(2, "visitante")
cursor2.execute(sql, datos)

conexion1.commit()    
conexion1.close()
