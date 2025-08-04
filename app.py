import chess
import tensorflow as tf
from tensorflow import keras
from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from ChessRun import *

app = Flask(__name__)
game = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board_page():
    return render_template('board.html')

@app.route('/reset')
def reset():
    global game
    game = chess.Board()
    return redirect(url_for('board_page'))

@app.route('/submit_move', methods=['POST'])
def move():
    player_move = request.get_json()
    print(player_move['move'])
    print("White Turn to Move")
    if make_move(player_move['move'], game):
        print("Success")
        return jsonify(success=True)
    else:
        print("illegal move")
        return jsonify(success=False)

@app.route("/update_state")
def get_board_state():
    return jsonify(board_current(game))

@app.route('/ai_move')
def ai_move():
    move = ai_select_move(game)
    print("ai move" + move)
    from_move = move[0:2]
    to_move = move[2:4]
    return jsonify(fromMove = from_move, toMove = to_move)