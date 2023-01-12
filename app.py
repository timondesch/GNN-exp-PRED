from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

original_list = [[["edge"], ["prediction"], ["PGM-explainer"]],
            [["edge"], ["classification"], ["subgraphx"]],
            [["node"], ["prediction"], ["GNNexplainer"]]]

backup_list = original_list

@app.route("/")
def home():
    print(original_list)
    return render_template("base.html", l=original_list)


@app.post("/add")
def add():
    title = request.form.get("title")
    original_list.append([[title], [title], [title]])
    backup_list.append([[title], [title], [title]])
    return redirect(url_for("home"))

@app.post("/filter")
def filter():
    global original_list
    title = request.form["filter"]
    original_list = [elem for elem in backup_list if elem[0] == [title]]
    return redirect(url_for("home"))