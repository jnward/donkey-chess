import chess
import chess.pgn

#state := board, next move, final result

#for game in file:
#  state = board, None, result
#  write state to file
#  while board is not initial:
#    undo last move
#    state = board, undone move, result
#    write state to file


with open("data/KingBaseLite2019-pgn/KingBaseLite2019-A00-A39.pgn") as pgn:
  while(True):
    game = chess.pgn.read_game(pgn)
    result = game.headers.get("Result")
    board = game.board()
    print(board)
    for move in game.mainline_moves():
      board.push(move)
      print("Result:", result)
      print(move)
      print(board.turn)

      #castling rights
      print(board.has_kingside_castling_rights(chess.WHITE))
      print(board.has_queenside_castling_rights(chess.WHITE))
      print(board.has_kingside_castling_rights(chess.BLACK))
      print(board.has_queenside_castling_rights(chess.BLACK))

      #material configuration
      print(len(board.pieces(chess.PAWN, chess.WHITE)))
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

      #piece lists
      



      

    print("\n")
