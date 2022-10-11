from crypt import methods
from importlib.metadata import requires
from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.exceptions import abort
from todo.auth import login_requiered
from todo.db import get_db 


bp = Blueprint('todo', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
@login_requiered
def index():
    db, c = get_db()
    c.execute(
        'select t.id,t.description,t.completed,t.created_by,t.created_at, u.username'
        ' from todo as t JOIN users as u on t.created_by = u.id where t.created_by = %s '
        ' order by created_at desc',(g.user['id'],)
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)
    
@bp.route('/create', methods=['GET','POST'])
@login_requiered
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None
        if not description:
            error = 'Descripcion es requerida'
            
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo (description, completed, created_by)'
                ' values (%s,%s,%s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id,t.description,t.completed,t.created_by,t.created_at, u.username from todo as t JOIN users as u on t.created_by = u.id where t.id = %s',(id,)
    )
    Eltodo = c.fetchone()
    
    if Eltodo is None:
        abort(404, 'El todo ya fue elinado, por ende no existe')

    return Eltodo

@bp.route('/<int:id>/update', methods=['GET','POST'])
@login_requiered
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None
        
        if not description:
            error = 'La descripcion es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s, completed =%s'
                ' where id=%s and created_by = %s',
                (description, completed, id,g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_requiered
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from todo where id = %s and created_by = %s',(id, g.user['id'])
    )
    db.commit()
    return redirect(url_for('todo.index'))