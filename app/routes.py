from urllib.request import Request
from flask import render_template, request, flash, redirect, url_for
from app import app
from json import loads
from copy import deepcopy
import re

board_name = ""
freeze_time = 240
problem_number = 12
team_dic = {}
'''
team_id : int -> {
  team_name : string
  team_member : string
  team_school : string
  is_star : bool
  submit_problem : dic {
    problem_id : int -> [
      used_time : int
      submit_number : int
      is_passed : bool
    ]
  }
  total_pass : int
  total_time : int
}
'''

submit_list = []
'''
team_id : int
submit_time : int (minutes from start) 
problem_id : int
result_id : int (should be sorted by submit_time)
            -1 : not pass but should not be calculated
            0 : not pass
            1 : pass
'''

freeze_submit = [] 
'''
[
  team_id : int
  {
    problem_id : dic -> [
      used_time : int
      submit_number : int
      is_passed : bool
    ]
  }
  total_pass : int
  total_time : int
]
'''

def Construct_Board() -> None:
  global team_dic, submit_list, freeze_submit
  freeze_submit = []
  team_dic = {team["team_id"] : team for team in team_dic}

  for team_id in team_dic :
    team_dic[team_id]["submit_problem"] = {}
    team_dic[team_id]["total_pass"] = team_dic[team_id]["total_time"] = 0
    for problem_id in range(1, problem_number + 1) :
      team_dic[team_id]["submit_problem"][problem_id] = [0, 0, False]

  for submit in submit_list :
    if submit["submit_time"] > freeze_time :
      freeze_submit.append(submit)
      continue
    if not team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][2] :
      if submit["result_id"] != -1 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][1] += 1
      if submit["result_id"] == 0 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][0] += 20
      elif submit["result_id"] == 1 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][0] += submit["submit_time"]
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][2] = True
        team_dic[submit["team_id"]]["total_pass"] += 1
        team_dic[submit["team_id"]]["total_time"] += team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][0]
  team_dic = {u : v for u, v in sorted(team_dic.items(), key = lambda item : (-item[1]["total_pass"], item[1]['total_time']))}

  rank = 1
  for team in team_dic :
    team_dic[team]["rank"] = rank
    rank += 1

  freeze_submit.sort(key = lambda item : team_dic[item["team_id"]]["rank"], reverse = True)
  freeze_temp = [] # [team_id, {problem_id -> used_time : int, submit_number : int, is_passed : bool}, total_pass, total_time]
  for submit in freeze_submit :
    if not freeze_temp or freeze_temp[-1][0] != submit["team_id"] :
      freeze_temp.append(deepcopy([submit["team_id"], team_dic[submit["team_id"]]["submit_problem"], 
                                   team_dic[submit["team_id"]]["total_pass"], team_dic[submit["team_id"]]["total_time"]]))
    if not freeze_temp[-1][1][submit["problem_id"]][2] :
      if submit["result_id"] != -1 :
        freeze_temp[-1][1][submit["problem_id"]][1] += 1
      if submit["result_id"] == 0 :
        freeze_temp[-1][1][submit["problem_id"]][0] += 20
      elif submit["result_id"] == 1 :
        freeze_temp[-1][1][submit["problem_id"]][0] += submit["submit_time"]
        freeze_temp[-1][1][submit["problem_id"]][2] = True
        freeze_temp[-1][2] += 1
        freeze_temp[-1][3] += freeze_temp[-1][1][submit["problem_id"]][0]
  freeze_submit = freeze_temp


@app.route('/Board')
def Scroll_Board() :
  Construct_Board()
  return render_template("Board.html", board_name = board_name, 
                                       board_head = ["rank", "team"] + [problem for problem in range(1, problem_number + 1)], 
                                       problem_number = problem_number,
                                       board = team_dic,
                                       freeze_submit = freeze_submit)

def check_file_name(file_name) -> bool :
  return re.match(".+\\.json", file_name) != None

def check_input_vailed() -> bool :
  ret = True
  if not check_file_name(request.files["team_data"].filename) :
    flash("No Team Data File")
    ret = False
  if not check_file_name(request.files["submit_data"].filename) :
    flash("No Submit Data File")
    ret = False
  if int(request.form["problem_number"]) <= 0 :
    flash("Invailed Problem Number")
    ret = False
  if int(request.form["freeze_time"]) < 0 :
    flash("Invailed Freeze Time")
    ret = False
  return ret

def load_input_file() -> None:
  global team_dic, submit_list, board_name, problem_number, freeze_time
  team_dic = loads(request.files["team_data"].stream.read())
  submit_list = loads(request.files["submit_data"].stream.read())
  board_name = request.form["board_name"]
  problem_number = int(request.form["problem_number"])
  freeze_time = int(request.form["freeze_time"])
  if board_name == "" :
    board_name = "ACM Contest"
  return None

@app.route('/', methods = ["GET", "POST"])
def index() :
  '''
  team_data.json example
  [
    {
      "team_id" : 1,
      "team_name" : "test1",
      "team_member" : "NONE", 
      "team_school" : "SCUT",
      "is_star" : false
    }
  ]
  submit_data.json example
  [
    {
      "team_id" : 1,
      "submit_time" : 100,
      "problem_id" : 1,
      "result_id" : 0
    }
  ]
  '''
  if request.method == "POST" :
    if not check_input_vailed() :
      return redirect(request.url) 
    load_input_file()
    return redirect(url_for("Scroll_Board"))
  else :
    return render_template("index.html")