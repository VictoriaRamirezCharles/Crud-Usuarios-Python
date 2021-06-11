import sqlite3
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_usuario(usuario_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?',
                        (usuario_id,)).fetchone()
    conn.close()
    if usuario is None:
        abort(404)
    return usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VRCHRCMCFHLCMRC'
@app.route('/')
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route('/<int:usuario_id>')
def usuario(usuario_id):
    usuario = get_usuario(usuario_id)
    return render_template('usuario.html', usuario=usuario)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        content = request.form['content']

        if not nombre:
            flash('nombre is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nombre, content) VALUES (?, ?)',
                         (nombre, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
@app.route('/<int:id>/edit', methods=('GET', 'POST'))

def edit(id):
    usuario = get_usuario(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        content = request.form['content']

        if not nombre:
            flash('nombre is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE usuarios SET nombre = ?, content = ?'
                         ' WHERE id = ?',
                         (nombre, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', usuario=usuario)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    usuario = get_usuario(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(usuario['nombre']))
    return redirect(url_for('index'))