from flask import Blueprint, render_template

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    #passing variables
    return render_template("index.html", name="phoebe")




