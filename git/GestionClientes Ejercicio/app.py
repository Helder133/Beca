from flask import Flask, render_template, request, redirect, url_for, flash
import pymssql

app = Flask(__name__)
app.secret_key = "supersecreto"

# Configuración de la base de datos MSSQL
DB_SERVER = "PC-DEV8"  # Cambia por tu servidor MSSQL
DB_DATABASE = "GestionClientes"
DB_USER = "Helder"
DB_PASSWORD = "Helder"

def get_db_connection():
    return pymssql.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE)

# Ruta para la página principal con la lista de clientes
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("EXEC sp_ObtenerClientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

# Ruta para agregar un nuevo cliente
@app.route('/agregar', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_InsertarCliente @Nombre=%s, @Email=%s, @Telefono=%s", 
                   (nombre, email, telefono))
    conn.commit()
    conn.close()
    
    flash('Cliente agregado correctamente', 'success')
    return redirect(url_for('index'))

# Ruta para eliminar un cliente
@app.route('/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_EliminarCliente @ClienteID=%s", (id,))
    conn.commit()
    conn.close()
    
    flash('Cliente eliminado correctamente', 'danger')
    return redirect(url_for('index'))

# Ruta para mostrar el formulario de edición
@app.route('/editar/<int:id>')
def editar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM Clientes WHERE ClienteID = %s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('editar.html', cliente=cliente)

# Ruta para actualizar un cliente
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_cliente(id):
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_ActualizarCliente @ClienteID=%s, @Nombre=%s, @Email=%s, @Telefono=%s",
                   (id, nombre, email, telefono))
    conn.commit()
    conn.close()
    
    flash('Cliente actualizado correctamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)