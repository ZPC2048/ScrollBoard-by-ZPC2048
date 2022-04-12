var problem_number, board, freeze_submit;
var index = 0, Board;

function get_data(PROBLEM_NUMBER, BOARD, FREEZE_SUBMIT) {
  problem_number = eval(PROBLEM_NUMBER);
  board = eval(BOARD);
  freeze_submit = eval(FREEZE_SUBMIT);
}

function getNewRow(id, row) {
  var html = "<tr id=" + id + ">";
  html += "<th>" + row["rank"] + "</th>";
  html += "<th>" + row["team_name"] + "</th>";
  for (var i in row["submit_problem"]) {
    var item = row["submit_problem"][i];
    if (item[2]) {
      if (item[1] == 1) {
        html += "<th> <p> + </p> <p> " + item[0] + " </p> </th>"
      } else {
        html += "<th> <p> + " + (item[1] - 1) + " </p> <p> " + item[0] + " </p> </th>"
      }
    } else {
      if (item[1] == 0) {
        html += "<th> <p></p> <p></p> </th>";
      } else if (item[1] == 1) {
        html += "<th> <p> - </p> <p></p> </th>";
      } else {
        html += "<th> <p> - " + item[1] + "</p> <p></p> </th>";
      }
    }
  }
  html += "</tr>";
  return html;
}

function cmp(row1, row2) {
  return row1["total_pass"] > row2["total_pass"] || (row1["total_pass"] == row2["total_pass"] && row1["total_time"] < row2["total_time"]);
}

function maintainTeamRank() {
  for (var i = 1; i < Board.rows.length - 1; ++i) {
    Board.rows[i].cells[0] = i;
  }
}

function moveRow(team_id) {
  board[team_id]["submit_problem"] = freeze_submit[index][1];
  board[team_id]["total_pass"] = freeze_submit[index][2];
  board[team_id]["total_time"] = freeze_submit[index][3];
  Board.deleteRow(document.getElementById(team_id).rowIndex);
  for (var i = Board.rows.length - 1; i >= 0; --i) {
    var temp_id = Board.rows[i].id;
    if (i == 0 || cmp(board[temp_id], board[team_id])) {
      Board.insertRow(i + 1).innerHTML = getNewRow(team_id, board[team_id]);
      break;
    }
  }
  ++index;
}

window.onclick = function() {
  Board = document.getElementById("Board");
  if (index >= freeze_submit.length) {
    alert("End!!!");
  } else {
    moveRow(freeze_submit[index][0]);
    maintainTeamRank();
  }
}