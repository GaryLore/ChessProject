import chess
import tensorflow as tf
from tensorflow import keras
from flask import Flask, render_template, jsonify, request, make_response
from ChessRun import *

app = Flask(__name__)
checkmate_model = keras.models.load_model("models/mate_model.keras")
evaluation_model = keras.models.load_model("models/epoch_20.keras")
game = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board():
    return render_template('board.html')

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