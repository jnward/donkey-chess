import chess
import chess.svg
from random import randint
#from flask import Flask, Response

from infer import infer_from_board

board_0 = chess.Board()


"""
app = Flask("__name__")

@app.route("/")
def hello():
  return "<html><body><img src='/board.svg'></img></body></html>"

@app.route("/board.svg")
def display_board():
  return Response(chess.svg.board(board_0), mimetype="image/svg+xml")

app.run()

"""

#board_0.push(list(board_0.legal_moves)[0])

MAX_DEPTH = 3

piece_dict = { "P" : 10,
               "p" : -10,
               "R" : 50,
               "r" : -50,
               "N" : 30,
               "n" : -30,
               "B" : 35,
               "b" : -35,
               "Q" : 90,
               "q" : -90,
               "K" : 1000,
               "k" : -1000
}

def play():
  print(board_0.unicode())
  while(True):
    #parse_user_move(board_0)
    make_computer_move_white(board_0)
    print(board_0.unicode())
    make_computer_move(board_0)
    #make_keras_move(board_0)
    print(board_0.unicode())
  
def parse_user_move(board):
  while(True):
    try:
      move_input = input("Move SAN: ")
      user_move = board.parse_san(move_input)
      break
    except ValueError:
      print("Invalid SAN")

  board.push(user_move)

def make_computer_move(board):
  move_list = list(board.legal_moves)
  num_moves = len(move_list)
  if num_moves == 0:
    print("Game over.")
  else:
    value, cpu_moves = minimax(board, MAX_DEPTH, False, -100000, 100000)
    print(value)
    for move in cpu_moves:
      print(move)
    print(board.san(cpu_moves[-1]))
    board.push(cpu_moves[-1])

def make_computer_move_white(board):
  move_list = list(board.legal_moves)
  num_moves = len(move_list)
  if num_moves == 0:
    print("Game over.")
  else:
    value, cpu_moves = minimax(board, MAX_DEPTH, True, -100000, 100000)
    print(value)
    for move in cpu_moves:
      print(move)
    print(board.san(cpu_moves[-1]))
    board.push(cpu_moves[-1])

def make_keras_move(board):
  move_list = list(board.legal_moves)
  num_moves = len(move_list)
  if num_moves == 0:
    print("Game over.")
  else:
    evals = []
    for move in move_list:
      board.push(move)
      logits = infer_from_board(board)[0]
      if not board.turn: #black to move
        logits = logits[::-1]
      evals.append(logits)
      board.pop()
    best_eval = 0
    best_move = None
    for i in range(len(move_list)):
      black_eval = evals[i][0]
      if black_eval > best_eval:
        best_eval = black_eval
        best_move = move_list[i]
      print(move_list[i], evals[i])
    board.push(best_move)


def minimax(board, depth, max_player, lower_bound, upper_bound):
  if depth == 0:
    return evaluate(board), []
  move_list = list(board.legal_moves)
  if len(move_list) == 0:
    return evaluate(board), []
  if max_player:
    value = -100000
    best_move = move_list[0]
    for move in move_list:
      board.push(move)
      new_value, moves = minimax(board, depth-1, False, lower_bound, upper_bound)
      board.pop()
      if new_value > value:
        value = new_value
        best_move = move
      if value > lower_bound:
        lower_bound = value
      if lower_bound >= upper_bound:
        break
    return value, moves + [best_move]
  else:
    value = 100000
    best_move = move_list[0]
    for move in move_list:
      board.push(move)
      new_value, moves = minimax(board, depth-1, True, lower_bound, upper_bound)
      board.pop()
      if new_value < value:
        value = new_value
        best_move = move
      if value < upper_bound:
        upper_bound = value
      if lower_bound >= upper_bound:
        break
    return value, moves + [best_move]

def _evaluate(board):
  value = 0
  if board.is_checkmate():
    if board.turn:
      return -10000
    else:
      return 10000
  for char in board.board_fen():
    value += piece_dict.get(char, 0)
  return value

def evaluate(board):
  logits = infer_from_board(board)[0]
  if not board.turn:
    logits = logits[::-1]
  return logits[2]
  


play()
