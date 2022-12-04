from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from .models import Note
from .forms import NoteCreationForm
from src.extensions import db
from flask_login import current_user
from datetime import datetime

notes = Blueprint('notes', __name__, template_folder='templates', static_folder='static')


@notes.route('/')
@login_required
def notes_list():
    page = request.args.get('page', 1, type=int)
    notes = db.session.query(Note).filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).paginate(
        page=page, per_page=7)
    return render_template('notes/notes-list.html', notes=notes)


@notes.route('/create', methods=['GET', 'POST'])
@login_required
def notes_create():
    form = NoteCreationForm()
    title = form.title.data
    description = form.description.data
    if form.validate_on_submit():
        current_date = datetime.now()
        note = Note(title=title, description=description, created_at=current_date, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes.notes_list'))
    return render_template('notes/notes-create.html', form=form)


@notes.route('/detail/<int:id>')
@login_required
def note_detail(id):
    note = db.session.query(Note).get(id)
    return render_template('notes/notes-detail.html', note=note)


@notes.route('/done/<int:id>')
@login_required
def note_done(id):
    note = db.session.query(Note).get(id)
    note.is_done = True
    db.session.commit()
    return redirect(url_for('notes.notes_list'))


@notes.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def note_edit(id):
    note = db.session.query(Note).get(id)
    form = NoteCreationForm(obj=note)
    if form.validate_on_submit():
        current_date = datetime.now()
        note.title = form.title.data
        note.description = form.description.data
        note.updated_at = current_date
        db.session.commit()
        return redirect(url_for('notes.notes_list'))
    return render_template('notes/notes_edit.html', form=form)


@notes.route('/delete/<int:id>')
@login_required
def note_delete(id):
    note = db.session.query(Note).get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.notes_list'))
