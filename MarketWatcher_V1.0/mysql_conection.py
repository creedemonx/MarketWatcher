import mysql.connector

import random
# Esto es solo una clase para poblar la base de datos con usuarios ficticios 
# No tiene ninguna relación con el resto del código mas que esta 
def populate_database():
    try:
        connection = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database="market_watcher",
            port=3306
        )
        cursor = connection.cursor()

        # Insertar 10 usuarios ficticios
        nombres = ["Luis", "Ana", "Carlos", "María", "Pedro", "Lucía", "Javier", "Carmen", "Miguel", "Laura"]
        apellidos = ["Gómez", "López", "Martínez", "Pérez", "Rodríguez", "Sánchez", "Fernández", "García", "Ruiz", "Vargas"]

        for _ in range(10):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            edad = random.randint(18, 65)
            correo = f"{nombre.lower()}.{apellido.lower()}@cristorey.com"
            contraseña = "1234"
            monto = random.uniform(1000, 10000)
	
            cursor.execute("""
                INSERT INTO users (nombre, apellido, edad, correo, contraseña, monto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, edad, correo, contraseña, monto))

        connection.commit()
        print("Base de datos poblada exitosamente con 10 usuarios.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

populate_database()
