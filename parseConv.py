import chess
import chess.pgn
import numpy as np

#state := board, next move, final result

#for game in file:
#  state = board, None, result
#  write state to file
#  while board is not initial:
#    undo last move
#    state = board, undone move, result
#    write state to file


with open("data/KingBaseLite2019-pgn/KingBaseLite2019-A00-A39.pgn") as pgn:
  game_num = 0
  while(True):
    game_num += 1
    game = chess.pgn.read_game(pgn)
    result = game.headers.get("Result")
    board = game.board()
    #print(board)
    for move in game.mainline_moves():
      board.push(move)
      #print("Result:", result)
      #print(move)
      #print(board.turn)
      #print(board)

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
      print(np.reshape(empty_squares, (8,8)))



      print(np.reshape(white_pawns_array, (8,8)))
      print(np.reshape(black_pawns_array, (8,8)))
      print(np.reshape(white_knights_array, (8,8)))
      print(np.reshape(black_knights_array, (8,8)))
      print(np.reshape(white_bishops_array, (8,8)))
      print(np.reshape(black_bishops_array, (8,8)))
      """
      #material configuration

      """
      print((board.pieces(chess.PAWN, chess.WHITE)))
      print(len(board.pieces(chess.KNIGHT, chess.WHITE)))
      print(len(board.pieces(chess.BISHOP, chess.WHITE)))
      print(len(board.pieces(chess.ROOK, chess.WHITE)))
      print(len(board.pieces(chess.QUEEN, chess.WHITE)))
      print(len(board.pieces(chess.KING, chess.WHITE)))
      print(len(board.pieces(chess.PAWN, chess.BLACK)))
      print(len(board.pieces(chess.KNIGHT, chess.BLACK)))
      print(len(board.pieces(chess.BISHOP, chess.BLACK)))
      print(len(board.pieces(chess.ROOK, chess.BLACK)))
      print(len(board.pieces(chess.QUEEN, chess.BLACK)))
      print(len(board.pieces(chess.KING, chess.BLACK)))
      """
      #piece lists
    if(game_num % 100 == 0):  
      print(game_num)



      

