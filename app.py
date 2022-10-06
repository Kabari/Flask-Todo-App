from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(base_dir,'todo.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean())

    def __repr__(self):
        return f" Title <{'self.title'}>"


@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

'''

Go to your terminal and type
Python then hit enter

# step 1
from app import app, db

# step 2
with app.app_context():

# step 3 After hitting enter in step 2, Press tab key and then type
db.create_all()

# Hit enter twice and boom your db is then created

'''
