from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env (si se usa)
# Esto permite mantener información sensible (como credenciales) fuera del código fuente.
# Recomendado por el profesor
load_dotenv()

# Configuración de la conexión a la base de datos utilizando variables de entorno
database = pymysql.connect(
    host=os.getenv('DB_HOST'),              # Dirección del servidor de la base de datos (obtenida de las variables de entorno)
    user=os.getenv('DB_USER'),              # Usuario autorizado para acceder a la base de datos
    password=os.getenv('DB_PASSWORD'),      # Contraseña del usuario
    database=os.getenv('DB_NAME'),          # Nombre de la base de datos
    cursorclass=pymysql.cursors.DictCursor  # Configuración para obtener resultados como diccionarios
)

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Ruta principal que muestra la lista de alumnos
@app.route("/")
def home():
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para obtener todos los registros de la tabla alumnos
    cursor.execute("SELECT * FROM alumnos")
    
    # Recuperar todos los resultados de la consulta como una lista de diccionarios
    users = cursor.fetchall()
 
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Renderizar la plantilla 'index.html' y pasar los datos de usuarios a la plantilla
    return render_template("index.html", data=users)

# Ruta para agregar un nuevo alumno
@app.route("/user", methods=['POST'])
def add_user():
    # Obtener los valores enviados desde el formulario HTML
    nombre = request.form["nombre"]  
    apellido = request.form["apellido"]
    aprobado = request.form["aprobado"]  
    nota = request.form["nota"]  
    
    # Verificar que los campos requeridos no estén vacíos
    if nombre and apellido and aprobado and nota:
        # Crear un cursor para interactuar con la base de datos
        cursor = database.cursor()
        
        # Ejecutar una consulta SQL para insertar un nuevo alumno
        cursor.execute(
            'INSERT INTO alumnos (nombre, apellido, aprobado, nota) VALUES (%s, %s, %s, %s)', 
            (nombre, apellido, aprobado, nota)
        )
        
        # Confirmar los cambios en la base de datos
        database.commit()
        
        # Cerrar el cursor para liberar recursos
        cursor.close()
    
    # Redirigir al usuario de nuevo a la página principal
    return redirect(url_for('home'))

# Ruta para eliminar un alumno
@app.route("/delete/<int:id>")
def delete_user(id):
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para eliminar un alumno por su ID
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id,))
    
    # Confirmar los cambios en la base de datos
    database.commit()
    
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Redirigir al alumno de nuevo a la página principal
    return redirect(url_for('home'))

# Ruta para mostrar detalles de un usuario específico
@app.route("/user/<int:id>")
def view_user(id):
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para obtener los datos de un alumno por su ID
    cursor.execute("SELECT * FROM alumnos WHERE id = %s", (id,))
    
    # Recuperar el resultado de la consulta (un único registro)
    user = cursor.fetchone()
    
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Verificar si el usuario existe
    if user:
        # Renderizar la plantilla 'user_detail.html' con los datos del alumno
        return render_template("user_detail.html", user=user)
    else:
        # Si no se encuentra el alumno, devolver un mensaje de error con el código HTTP 404
        return "Usuario no encontrado", 404

# Ruta para editar los datos de un alumno
@app.route("/edit/<int:id>", methods=['POST'])
def edit_user(id):
    # Obtener los valores enviados desde el formulario HTML
    nombre = request.form["nombre"]  
    apellido = request.form["apellido"]      
    aprobado = request.form["aprobado"]  
    nota = request.form["nota"]  
    # Verificar que los campos requeridos no estén vacíos
    if nombre and apellido and aprobado and nota:
        # Crear un cursor para interactuar con la base de datos
        cursor = database.cursor()
        
        # Ejecutar una consulta SQL para actualizar los datos del alumno
        cursor.execute(
            'UPDATE alumnos SET nombre = %s, apellido = %s, aprobado = %s, nota= %s  WHERE id = %s', 
            (nombre, apellido, aprobado, nota, id)
        )
        
        # Confirmar los cambios en la base de datos
        database.commit()
        
        # Cerrar el cursor para liberar recursos
        cursor.close()
    
    # Redirigir al usuario de nuevo a la página principal
    return redirect(url_for('home'))

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecutar la aplicación en modo de depuración para desarrollo
    # Escucha en el puerto 5000 por defecto
    app.run(debug=True, port=5000)
