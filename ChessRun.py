
import chess
from tabulate import tabulate
from fenConversion import*
import tensorflow as tf
from tensorflow import keras
import time


def print_board(board):
    start = "\033[1;93m"
    end = "\033[0m"
    header = [' ', start + 'a' + end, start + 'b' + end, start + 'c' + end, start + 'd' + end, start + 'e' + end, start + 'f' + end, start + 'g' + end, start + 'h' + end]

    rows_info = []
    for row in range(8, 0, -1):
        row_info = [start + str(row) + end]
        for col in range(8):
            square = chess.square(col, row - 1)
            piece = board.piece_at(square)
            row_info.append(piece.symbol() if piece else ' ')
        rows_info.append(row_info)

    table = tabulate(rows_info, header, tablefmt="heavy_grid")
    print(table)

def board_current(board):
    board_state = {}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:#only if piece is not none
            board_state[chess.square_name(square)] = piece.symbol()

    
    print("LOOK HEREEEEEEEEEEEEEEEEE")
    print(board_state)
    return board_state

#not needed anymore but kept just in case
def select_piece():

    while True:
        piece = input('Choose Piece to move: ')
        square = chess.parse_square(piece)
        piece_moves = [move for move in board.legal_moves if move.from_square == square]

        if piece_moves:
            break
        else:
            print('Choose a LEGAL Piece')

    return piece

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

def ai_select_move(temp_board, black=True):

    possible_moves = list(board.legal_moves)

    input_list = []
    for move in possible_moves:
        temp_board.push(move)
        fen = board.fen()
        input = FENParser(fen)
        input_list.append(input.parse())
        temp_board.pop()

    X = np.array(input_list)

    moves_index_eval = run_checkmate_model(X)#moves index worth evaluating
    #print('Num of moves that are worth evaluating:')
    #print(len(moves_index_eval))
    if len(moves_index_eval) > 1:

        eval_positions=[]#will contain inputs that are worth evalating
        for index in moves_index_eval:

            move = possible_moves[index]#move worth evaluating
            temp_board.push(move)
            fen = board.fen()
            input = FENParser(fen)
            eval_positions.append(input.parse())
            temp_board.pop()

        index_of_eval_positions = run_eval_model(np.array(eval_positions))#returns index of eval_positions which is the same index for a position as moves_index_eval
        best_move_index = moves_index_eval[index_of_eval_positions]#gets index of move using moves_index_eval
        best_move = possible_moves[best_move_index]

    else:
        best_move = possible_moves[moves_index_eval[0]]

    board.push(best_move)

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

if __name__ == "__main__":
    checkmate_model = keras.models.load_model("models/mate_model.keras")
    evaluation_model = keras.models.load_model("models/eval_big_model_v2.keras")
    board = chess.Board()

    while True:

        print()
        print_board(board)

        if board.turn == chess.WHITE:

            print("White Turn to Move")
            start = select_piece()
            make_move(start)
            print()

        else:
            
            time.sleep(1.5)#time delay so you can actually see what you moved 
            print("Black Has Moved")
            ai_select_move(board)

        result = board.result()
        if result != "*":
            print_board(board)
            print(result)
            break
