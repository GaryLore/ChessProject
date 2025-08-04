
import chess
from tabulate import tabulate
from fenConversion import*
import tensorflow as tf
from tensorflow import keras
import time

def board_current(board):
    board_state = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:#only if piece is not none
            board_state[chess.square_name(square)] = piece.symbol()

    
    print("LOOK HEREEEEEEEEEEEEEEEEE")
    print(board_state)
    return board_state

#modified
def make_move(player_move, board):
    print("make move entered")
    while True:
        move = chess.Move.from_uci(player_move)
        if board.is_legal(move):
            board.push(move)
            print("make move PUSHED")
            return True
        else:
            return False

def ai_select_move(board, black=True):

    possible_moves = list(board.legal_moves)

    input_list = []
    for move in possible_moves:
        board.push(move)
        fen = board.fen()
        input = FENParser(fen)
        input_list.append(input.parse())
        board.pop()

    X = np.array(input_list)

    moves_index_eval = run_checkmate_model(X)#moves index worth evaluating
    #print('Num of moves that are worth evaluating:')
    #print(len(moves_index_eval))
    if len(moves_index_eval) > 1:

        eval_positions=[]#will contain inputs that are worth evalating
        for index in moves_index_eval:

            move = possible_moves[index]#move worth evaluating
            board.push(move)
            fen = board.fen()
            input = FENParser(fen)
            eval_positions.append(input.parse())
            board.pop()

        index_of_eval_positions = run_eval_model(np.array(eval_positions))#returns index of eval_positions which is the same index for a position as moves_index_eval
        best_move_index = moves_index_eval[index_of_eval_positions]#gets index of move using moves_index_eval
        best_move = possible_moves[best_move_index]

    else:
        best_move = possible_moves[moves_index_eval[0]]

    board.push(best_move)
    first = chess.square_name(best_move.from_square)#returning string part of move to get square start from
    second = chess.square_name(best_move.to_square)
    return first+second

# returns a list of possible good moves to further evaluate, specifically returning the indexes of eval_positions that are worth evaluating
#and these same indexes correspond to the moves_index_eval index, which can then be used to access the moves[using the index]
#moves_index_eval[] and eval_position[]  a single index here corresponds to each other for example eval_position[2] is the evaluation position of moves_index_eval[2]
def run_checkmate_model(X, black=True):
    Y = checkmate_model.predict_on_batch(X)
    indexes = np.argmax(Y, axis=1) # 1 if forced mate for black, 2 if forced mate for white, 0 no forced mate

    i = 0
    selected_position_indexes = []
    alternatives = []

    if black:
        for index in indexes:
            if index == 1:#forced mate for black preferred
                selected_position_indexes = [i]
                break
            elif index == 0:#append if its not forced mate
                selected_position_indexes.append(i)
            elif index == 2:
                alternatives.append(i)

            i +=1

    else:
        print('functionality for white hasnt been implemented yet')

    if len(selected_position_indexes) == 0:#edge case if there are no good moves for black we have to still give it a index to move
        selected_position_indexes.append(alternatives[0])#so we just choose the first alternative

    return selected_position_indexes

def run_eval_model(X):

    Y = evaluation_model.predict_on_batch(X)
    #returns 2d numpy array so [[1],[1],[1]] but each array in the array is only one length

    i = 0
    centipawn = Y[0]
    pos_index = 0

    for pred_value in Y:
        if pred_value[0] < centipawn:
            centipawn = pred_value[0]
            pos_index = i

        i +=1

    return pos_index

checkmate_model = keras.models.load_model("models/mate_model.keras")
evaluation_model = keras.models.load_model("models/epoch_20.keras")

