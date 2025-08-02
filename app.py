import chess
import tensorflow as tf
from tensorflow import keras
from flask import Flask, render_template
from ChessRun import *

app = Flask(__name__)
checkmate_model = keras.models.load_model("models/mate_model.keras")
evaluation_model = keras.models.load_model("models/epoch_20.keras")
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/move', methods=['POST'])
def move():
    pass