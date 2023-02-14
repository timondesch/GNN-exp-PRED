from flask import Flask, render_template, request, redirect, url_for
from ontology import *

app = Flask(__name__)

base_status = ""
original_list = []

backup_list = original_list

@app.route("/")
def home():
    return render_template("base.html", l=original_list, s=base_status)


@app.post("/add")
def add():
    title = request.form.get("title")
    original_list.append([[title], [title], [title]])
    return redirect(url_for("home"))

@app.post("/filter")
def filter():
    global original_list, base_status
    title = request.form

    print(title)
    tmp_list = [x[0] for x in sparql_query(title["format"], title["task"])]
    original_list = tmp_list
    print(tmp_list)
    base_status = f"explaining {label_query(title['task']).describe()} with {label_query(title['format']).describe()}."
    return redirect(url_for("home"))