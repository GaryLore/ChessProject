import chess
import tensorflow as tf
from tensorflow import keras
from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for, session
from ChessRun import *

app = Flask(__name__)
app.secret_key = "2925942692912a3f983e48b1d5ed066915a4a9d2851846e0d2a150db199b7549"
app.config.update(
    SECRET_KEY=app.secret_key,   # Loaded from environment
    SESSION_COOKIE_SECURE=True,                # Cookie sent only over HTTPS
    SESSION_COOKIE_HTTPONLY=True,              # JS can't access cookie
    SESSION_COOKIE_SAMESITE="Lax"              # Blocks cross-site requests
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board_page():
    if "FEN" not in session:
        session["FEN"] = chess.Board().fen()##assigns default fen

    return render_template('board.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/reset')
def reset():
    session["FEN"] = chess.Board().fen()##assigns default fen
    return redirect(url_for('board_page'))

@app.route('/submit_move', methods=['POST'])
def move():
    game = initializeBoard()
    player_move = request.get_json()
    print(player_move['move'])
    print("White Turn to Move")
    if make_move(player_move['move'], game):
        session["fen"] = game.fen()
        print("Success")
        session["FEN"] = game.fen()
        return jsonify(success=True)
    else:
        print("illegal move")
        return jsonify(success=False)

@app.route("/update_state")
def get_board_state():
    print("TESTING SESSION COOKIE:  " + session["FEN"])
    game = initializeBoard()
    if game.is_game_over():
        info = game.outcome()
        print("Game termination : " + str(info.termination))

        playerWon = info.winner
        player = ""
        if playerWon is None:
            player = "DRAW"
        elif playerWon == chess.WHITE:
            player = "WHITE"
        elif playerWon == chess.BLACK:
            player = "BLACK"

        response_data = {
        "board": board_current(game),
        "end": True,
        "winner": player
        }
        return jsonify(response_data)

    response_data = {
        "board": board_current(game),
        "check": game.is_check(),
        "end": False,
        "winner": "NONE"
        }
    return jsonify(response_data)

@app.route('/ai_move')
def ai_move():
    game = initializeBoard()
    move = ai_select_move(game)
    print("ai move" + move)
    from_move = move[0:2]
    to_move = move[2:4]
    session["FEN"] = game.fen()
    return jsonify(fromMove = from_move, toMove = to_move)

def initializeBoard():
    return chess.Board(session["FEN"])