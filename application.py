from flask import Flask, render_template, session, redirect
from flask_session import Session 
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    is_tie = False

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["next"] = "O"
        session["winner"] = None
        session["count"] = 0

    else:
        b = session["board"]
        n = session["next"]
        count = session["count"]
        
        # rows
        if (b[0][0] == b[0][1] == b[0][2] == n) or (b[1][0] == b[1][1] == b[1][2] == n) or (b[2][0] == b[2][1] == b[2][2] == n):
            session["winner"] = n

        # cols
        elif (b[0][0] == b[1][0] == b[2][0] == n) or (b[0][1] == b[1][1] == b[2][1] == n) or (b[0][2] == b[1][2] == b[2][2] == n):
            session["winner"] = n        

        # diags
        elif (b[0][0] == b[1][1] == b[2][2] == n) or (b[0][2] == b[1][1] == b[2][0] == n):
            session["winner"] = n

        # tie
        elif count == 9:
            is_tie = True

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"], is_tie=is_tie)


@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    session["board"][row][col] = session["turn"]
    session["count"] += 1

    if session["turn"] == "X": 
        session["turn"] = "O"
        session["next"] = "X"
    else:
        session["turn"] = "X"
        session["next"] = "O"

    return redirect("/")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

some new feature