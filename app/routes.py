from flask import render_template, request, flash, redirect, url_for
from app import app
from json import loads
from functools import cmp_to_key
import re

board_name = ""
freeze_time = 200
problem_number = 5
team_dic = {} #team_id as int, team_name, team_member, team_school, is_star as bool, (submit_problem(problem_id -> used_time, submit_number, is_passed), total_pass, total_time)
submit_list = [] #team_id as int, submit_time(minutes from start) as int, problem_id as int, result_id as int (should be sorted by submit_time)
'''
result_id 
-1 not pass but should not be calculated
0 not pass
1 pass
'''

def check_file_name(file_name) -> bool :
  return re.match(".+\\.json", file_name) != None

def Construct_Board() :
  global team_dic
  team_dic = {team["team_id"] : team for team in team_dic}
  for team_id in team_dic :
    team_dic[team_id]["submit_problem"] = {}
    team_dic[team_id]["total_pass"] = team_dic[team_id]["total_time"] = 0
    for problem_id in range(1, problem_number + 1) :
      team_dic[team_id]["submit_problem"][problem_id] = [0, 0, False]
  for submit in submit_list :
    if submit["submit_time"] > freeze_time :
      break
    if not team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][2] :
      if submit["result_id"] != -1 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][1] += 1
      if submit["result_id"] == 0 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][0] += 20
      elif submit["result_id"] == 1 :
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][0] += submit["submit_time"]
        team_dic[submit["team_id"]]["submit_problem"][submit["problem_id"]][2] = True
        team_dic[submit["team_id"]]["total_pass"] += 1
  return {u : v for u, v in sorted(team_dic.items(), 
                                    key = cmp_to_key(lambda item1, item2 : item1[1]["total_time"] < item2[1]["total_time"]  
                                                                          if item1[1]["total_pass"] != item2[1]["total_pass"] 
                                                                          else item1[1]["total_pass"] < item2[1]["total_pass"]))}



@app.route('/Board')
def Scroll_Board() :
  # print(Construct_Board())
  return render_template("Board.html", board_name = board_name, 
                                       board_head = ["rank", "team"] + [problem for problem in range(1, problem_number + 1)], 
                                       board = Construct_Board())

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
    global team_dic 
    team_dic = loads(request.files["team_data"].stream.read())
    global submit_list 
    submit_list = loads(request.files["submit_data"].stream.read())
    if board_name == "" :
      board_name = "Programming Contest"
    return redirect(url_for("Scroll_Board"))
  else :
    return render_template("index.html")