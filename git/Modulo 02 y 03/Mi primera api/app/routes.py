from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Usuario

# Definir el Blueprint
main_bp = Blueprint('main', __name__)

# Página principal - Lista de usuarios
@main_bp.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

# Formulario para agregar usuario
@main_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        edad = request.form['edad']

        nuevo_usuario = Usuario(nombre=nombre, correo=correo, edad=edad)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add_user.html')

# Formulario para editar usuario
@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        usuario.edad = request.form['edad']

        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit_user.html', usuario=usuario)

# Eliminar usuario
@main_bp.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('main.index'))