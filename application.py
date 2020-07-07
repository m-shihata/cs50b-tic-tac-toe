import os
from flask import Flask, render_template, session, redirect
from helpers import score, best_move
from flask_session import Session
import pylibmc

app = Flask(__name__)

servers = os.environ.get('MEMCACHIER_SERVERS').split(',')
username = os.environ.get('MEMCACHIER_USERNAME')
passwd = os.environ.get('MEMCACHIER_PASSWORD')

app.config.from_mapping(
    SESSION_TYPE = 'memcached',
    SESSION_MEMCACHED =
        pylibmc.Client(servers, binary=True,
                       username=username, password=passwd,
                       behaviors={
                            # Faster IO
                            'tcp_nodelay': True,
                            # Keep connection alive
                            'tcp_keepalive': True,
                            # Timeout for set/get requests
                            'connect_timeout': 2000, # ms
                            'send_timeout': 750 * 1000, # us
                            'receive_timeout': 750 * 1000, # us
                            '_poll_timeout': 2000, # ms
                            # Better failover
                            'ketama': True,
                            'remove_failed': 1,
                            'retry_timeout': 2,
                            'dead_timeout': 30,
                       })
)

Session(app)

@app.route("/")
def index():

    s = None

    # New session
    if "board" not in session:
        session["board"] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        session["turn"] = 1
        session["count"] = 0
        session["stack"] = []

    # Continue until Winner or Tie 
    else:
        s = score(session["board"], session["turn"], session["count"])

    return render_template("game.html", game=session["board"], turn=session["turn"], score=s, count=session["count"])


@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # play
    session["board"][row][col] = session["turn"]
    session["count"] += 1
    session["stack"].append((row, col))

    # swich players 
    session["turn"] *= -1

    return redirect("/")


@app.route("/undo")
def undo():

    # Undo
    last_move = session["stack"].pop()
    session["board"][last_move[0]][last_move[1]] = 0
    session["count"] -= 1

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
    game = session["board"] 

    # Find the best move
    m = best_move(game, session["turn"], session["count"])

    # Play it 
    return redirect(f"play/{m[0]}/{m[1]}")


@app.route("/auto")
def auto():

    # clone the board to create a safe area for figuring things out 
    game = session["board"] 

    # Find the best move
    m = best_move(game, session["turn"], session["count"])

    # Play it 
    return redirect(f"play/{m[0]}/{m[1]}")