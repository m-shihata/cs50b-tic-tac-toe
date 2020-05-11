from flask import Flask, render_template, session, redirect
from flask_session import Session 
from tempfile import mkdtemp
from helpers import Score, Best_move
from copy import deepcopy


app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():

    score = None

    # New session
    if "board" not in session:
        session["board"] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
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

    # Reset game to square 0
    session.clear()
    return redirect("/")


@app.route("/play")
def play_computer():

    # clone the board to create a safe area for figuring things out 
    game = deepcopy(session["board"]) 

    # Find the best move
    move = Best_move(game, session["turn"], session["count"])

    # Play it 
    return redirect(f"play/{move[0]}/{move[1]}")