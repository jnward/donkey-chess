import chess
import chess.pgn
import numpy as np
import csv
from os import walk

import random
#state := board, next move, final result

#for game in file:
#  state = board, None, result
#  write state to file
#  while board is not initial:
#    undo last move
#    state = board, undone move, result
#    write state to file
def generate_input_vec():
  white_pawns = board.pieces(chess.PAWN, chess.WHITE)
  white_pawns_array = np.zeros(64)
  white_pawns_array[list(white_pawns)] = True
  white_knights = board.pieces(chess.KNIGHT, chess.WHITE)

  white_knights_array = np.zeros(64)
  white_knights_array[list(white_knights)] = True
  white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
  white_bishops_array = np.zeros(64)
  white_bishops_array[list(white_bishops)] = True

  white_rooks = board.pieces(chess.ROOK, chess.WHITE)
  white_rooks_array = np.zeros(64)
  white_rooks_array[list(white_rooks)] = True

  white_queens = board.pieces(chess.QUEEN, chess.WHITE)
  white_queens_array = np.zeros(64)
  white_queens_array[list(white_queens)] = True

  white_kings = board.pieces(chess.KING, chess.WHITE)
  white_kings_array = np.zeros(64)
  white_kings_array[list(white_kings)] = True

  black_pawns = board.pieces(chess.PAWN, chess.BLACK)
  black_pawns_array = np.zeros(64)
  black_pawns_array[list(black_pawns)] = True

  black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
  black_knights_array = np.zeros(64)
  black_knights_array[list(black_knights)] = True

  black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
  black_bishops_array = np.zeros(64)
  black_bishops_array[list(black_bishops)] = True

  black_rooks = board.pieces(chess.ROOK, chess.BLACK)
  black_rooks_array = np.zeros(64)
  black_rooks_array[list(black_rooks)] = True

  black_queens = board.pieces(chess.QUEEN, chess.BLACK)
  black_queens_array = np.zeros(64)
  black_queens_array[list(black_queens)] = True

  black_kings = board.pieces(chess.KING, chess.BLACK)
  black_kings_array = np.zeros(64)
  black_kings_array[list(black_kings)] = True

  pawns_array = white_pawns_array - black_pawns_array
  knights_array = white_knights_array - black_knights_array
  bishops_array = white_bishops_array - black_bishops_array
  rooks_array = white_rooks_array - black_rooks_array
  queens_array = white_queens_array - black_queens_array
  kings_array = white_kings_array - black_kings_array
  #print(np.reshape(pawns_array, (8,8)))

  empty_squares = 1 - (white_pawns_array + 
                       white_knights_array +
                       white_bishops_array +
                       white_rooks_array +
                       white_queens_array +
                       white_kings_array +
                       black_pawns_array +
                       black_knights_array +
                       black_bishops_array +
                       black_rooks_array +
                       black_queens_array +
                       black_kings_array)
  """  
  print("orgiginal \n")
  print(np.reshape(pawns_array, (8,8)))
  """
  if not board.turn: #flip board if it's black's turn so we don't need to encode this info
    pawns_array = np.flipud(-np.reshape(pawns_array, (8,8))).flatten()
    knights_array = np.flipud(-np.reshape(knights_array, (8,8))).flatten()
    bishops_array = np.flipud(-np.reshape(bishops_array, (8,8))).flatten()
    rooks_array = np.flipud(-np.reshape(rooks_array, (8,8))).flatten()
    queens_array = np.flipud(-np.reshape(queens_array, (8,8))).flatten()
    kings_array = np.flipud(-np.reshape(kings_array, (8,8))).flatten()
    empty_squares = np.flipud(np.reshape(empty_squares, (8,8))).flatten()
    #gotta flip the move too
  """  
  """
  #piece lists
  input_vec = np.concatenate([pawns_array,
                             knights_array,
                             bishops_array,
                             rooks_array,
                             queens_array,
                             kings_array,
                             empty_squares])
  #print(np.reshape(input_vec, (7,8,8)))
  input_vec = input_vec.astype(int)

  return input_vec

data_path = "data/kingbase-lite-2019"
in_files = []
for path, dirs, files in walk(data_path):
  in_files = files
  break
print(in_files)
print("files^^^")
for file in in_files:
  print(file)

for i, file in enumerate(in_files):
  with open(data_path + "/" + file) as pgn:
    game_num = 0
    with open('data/parsed_games_aug2/parsed_' + str(i), 'w') as out:
      writer = csv.writer(out, delimiter=',')
      while(True):
        game_num += 1
        #print(game_num)
        try:
            game = chess.pgn.read_game(pgn)
        except:
            break
        result = game.headers.get("Result")
        event = game.headers.get("Event")
        out_batch = []
        if "blitz" in event.lower():
          continue
        elif "rapid" in event.lower():
          continue
    
        #print(event)
        board = game.board()
        #print(board)
        for movenum, move in enumerate(game.mainline_moves()):
    
          #board.push(move)
          #print("Result:", result)
          #print(move)
          #print(board.turn)
          #print(board)
          flip = False
          if random.random() > 0.8 and result == '1-0':
            flip = True


          if flip:
            board.turn = not board.turn

          input_vec = generate_input_vec()
          if flip:
            board.turn = not board.turn 
  
          #flip move
          if not board.turn:
            flip_move = []
            for i,c in enumerate(move.uci()):
              if(i%2):
                char = str(9-int(c))
              else:
                char = c
              flip_move += [char]
            out_move = ''.join(flip_move)
          else:
            out_move = move.uci()
  
          try:      
            if len(result) == 7:
              out_result = 0
            else:
              if board.turn:
                #white to move
                out_result = 2*int(result[0])-1
              else:
                out_result = -2*int(result[0])+1
          except:
              break

          if flip:
            out_result = 1

          #out_batch.append(np.concatenate([input_vec,[out_move,out_result]]))
  
          
          out_array = np.concatenate([[out_result], input_vec])
  
          writer.writerow(out_array)
  
          #fileName = str(game_num*1000+movenum)
  
            #np.save('data/npfiles/%s'%(fileName),out_array)
  
          board.push(move)
  
        input_vec = generate_input_vec()
  
        #out_batch.append(np.concatenate([input_vec,["0000", out_result]]))
  
        out_array = np.concatenate([[out_result], input_vec])
  
        writer.writerow(out_array) 
  
        #fileName = str(game_num*1000+999)
  
        #np.save('data/npfiles/%s'%(fileName),out_array)



        #writer.writerows(out_batch)
        if(game_num % 10 == 0):  
          print(game_num)
          #print(input_vec)
        

      
