import chess
import chess.pgn
import csv

from keras.models import Model, load_model
from keras.layers import *
from keras.optimizers import Adam
from keras import regularizers
from keras.callbacks import ModelCheckpoint

import numpy as np

model = load_model('models/model-07-0.480.hdf5')

def generate_input_vec(board):
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

def create_model():

  inputs = Input(shape=(7,8,8))
  y = res_block(y=inputs, nb_channels=32)
  y = res_block(y=y, nb_channels=32, _project_shortcut=False)
  y = res_block(y=y, nb_channels=32, _project_shortcut=False)
  y = res_block(y=y, nb_channels=32, _project_shortcut=False)
  y = res_block(y=y, nb_channels=32, _project_shortcut=False)     
  #y = Conv2D(32,kernel_size=(5,5),data_format='channels_first',batch_size=params['batch_size']$
  #y = LeakyReLU()(y)
  y = Flatten()(y)
  y = Dense(128, activation=None)(y)
  #y = LeakyReLU()(y)
  outputs = Dense(3, activation='softmax', kernel_regularizer=regularizers.l2(0.00005))(y)

  model = Model(inputs=inputs, outputs=outputs)

        
  adam = Adam(lr=0.00002)
  model.compile(optimizer=adam,
                loss='categorical_crossentropy',
                metrics=['accuracy'])

  print(model.summary())

def res_block(y, nb_channels, _strides=(1,1), _project_shortcut=True):
  shortcut = y

  y = Conv2D(nb_channels, kernel_size=(4,4), strides=_strides, padding='same', data_format='channels_first')(y)
  y = BatchNormalization()(y)
  y = LeakyReLU()(y)

  y = Conv2D(nb_channels, kernel_size=(4,4), strides=(1,1), padding='same', data_format='channels_first')(y)
  y = BatchNormalization()(y)
  y = LeakyReLU()(y)

  if _project_shortcut:
    shortcut = Conv2D(nb_channels, kernel_size=(1,1), strides=_strides, padding='same', data_format='channels_first')(shortcut)

  y = add([shortcut, y])
	#y = LeakyReLU()(y)

  return y

def infer():
  #model = load_model('models/model-07-0.480.hdf5')

  #pgn_file = open('data/')

  file = open('data/parsed_games/parsed_1', 'r')

  reader = csv.reader(file, delimiter=',')

  create_model()
  for board in reader:
    datum = np.array([int(string) for string in board[1:]])
    label = int(board[0])+1

    in_vec = np.reshape(datum, (1,7,8,8))

    #print(in_vec, label)

    logits = model.predict(in_vec, verbose=1)
    print(logits, label)
    #break

def infer_from_board(board):
  in_vec = generate_input_vec(board)

  in_vec = np.reshape(in_vec, (1,7,8,8))

  logits = model.predict(in_vec, verbose=0)

  return logits

if __name__ == "__main__":

  board = chess.Board()
  while True:
    print(infer_from_board(board))
  #infer()