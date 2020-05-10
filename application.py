from flask import Flask, render_template, session, redirect
from flask_session import Session 
from tempfile import mkdtemp
from helpers import score

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    Score = None

    # New session
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = 1
        session["count"] = 0

    # Continue until Winner or Tie 
    else:
        score = Score(session["board"], session["turn"], session["count"])

    return render_template("game.html", game=session["board"], turn=session["turn"], score=score)


@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # play
    session["board"][row][col] = session["turn"]
    session["count"] += 1

    # swich players 
    session["turn"] *= -1

    return redirect("/")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


@app.route("/play")
def play_computer():
    pass