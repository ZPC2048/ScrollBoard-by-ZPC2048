from flask import render_template, request, flash, redirect, url_for
from app import app
from json import loads
import re

board_name = ""
team_dic = {} #team_id -> team_name, team_member, team_school
submit_list = [] #submit_id, submit_time, problem_id, result_id

def check_file_name(file_name) -> bool :
  return re.match(".+\\.json", file_name) != None

@app.route('/Board')
def Scroll_Board() :
  team_dic = [["1", "test"], ["2", "hello"]]
  return render_template("Board.html", board_name = board_name, board_head = {"team_id", "team_name"}, board = team_dic)

@app.route('/', methods = ["GET", "POST"])
def index() :
  if request.method == "POST" :
    is_team_file_vailed = check_file_name(request.files["team_data"].filename)
    is_submit_file_vailed = check_file_name(request.files["submit_data"].filename) 
    if not is_team_file_vailed or not is_submit_file_vailed :
      if not is_team_file_vailed :
        flash("No Team Data File")
      if not is_submit_file_vailed :
        flash("No Submit Data File")
      return redirect(request.url) 
    board_name = request.form["board_name"]
    team_dic = loads(request.files["team_data"].stream.read())
    submit_list = loads(request.files["submit_data"].stream.read())
    if board_name == "" :
      board_name = "Programming Contest"
    return redirect(url_for("Scroll_Board"))
  else :
    return render_template("index.html")