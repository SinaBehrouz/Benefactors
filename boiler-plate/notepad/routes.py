from flask import render_template, url_for, flash, redirect, request
from notepad import app, db
from notepad.forms import NoteForm, UpdateForm
from notepad.models import Note


@app.route("/")
@app.route("/home")
def home():
    notes = Note.query.all()
    return render_template('home.html', notes=notes)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/note/new", methods=['GET', 'POST'])
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(author=form.author.data, title=form.title.data, content=form.content.data)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_note.html', title='New Note', form=form, legend='New Note')


@app.route("/note/<int:note_id>")
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', title=note.title, note=note)


@app.route("/note/<int:note_id>/update", methods=['GET', 'POST'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = UpdateForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', title='Update Note', form=form, legend='Update Note')


@app.route("/note/<int:note_id>/delete", methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('home'))
