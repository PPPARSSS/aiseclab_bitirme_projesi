from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'
    pk_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    complete_status = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form['title']
    desc = request.form['desc']
    complete_status = False
    new_todo = Todo(title=title, desc=desc, complete_status=complete_status)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:pk_id>", methods=["GET", "POST"])
def edit(pk_id):
    todo = Todo.query.get(pk_id)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo)

@app.route("/check/<int:pk_id>", methods=["GET", "POST"])
def check(pk_id):
    todo = Todo.query.get(pk_id)
    if request.method == "POST":
        todo.complete_status = not todo.complete_status
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:pk_id>", methods=["GET", "POST"])
def delete(pk_id):
    todo = Todo.query.get(pk_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
