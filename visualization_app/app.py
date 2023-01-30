from flask import Flask, render_template, request, redirect, url_for
from ontology import *

app = Flask(__name__)

original_list = [[["edge"], ["prediction"], ["PGM-explainer"]],
            [["edge"], ["classification"], ["subgraphx"]],
            [["node"], ["prediction"], ["GNNexplainer"]]]

original_list = [{"name":"Enter some criteria to get started."}]

base_status = ""

backup_list = original_list

@app.route("/")
def home():
    return render_template("base.html", l=original_list, s=base_status)


@app.post("/add")
def add():
    title = request.form.get("title")
    original_list.append([[title], [title], [title]])
    return redirect(url_for("home"))

# @app.post("/filter")
# def filter():
#     global original_list
#     title = request.form
#     if len(title) == 0: original_list = backup_list
#     else: original_list = [elem for elem in backup_list if elem[0] == [title["filter"]]]
#     return redirect(url_for("home"))

@app.post("/filter")
def filter():
    global original_list, base_status
    title = request.form

    print(title)
    tmp_list = sparql_query(title["format"], title["task"])
    original_list = tmp_list
    original_list = [x[0].details() for x in tmp_list]
    print(title)
    base_status = f"explaining {label_query(title['task']).describe()} with {label_query(title['format']).describe()}."
    return redirect(url_for("home"))