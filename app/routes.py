from flask import render_template, request, flash, redirect, url_for
from app import app

# def 

@app.route('/', methods = ["GET", "POST"])
def index() :
  if request.method == "POST" :
    print(request.files)
    print(request.files.getlist("upload_file"))
    if "file" not in request.files or request.files["file"].filename == "":
      flash("No File")
      return redirect(request.url) 
    return "??"
  else :
    return render_template("index.jinja")