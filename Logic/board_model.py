from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import regularizers
import numpy as np
import matplotlib.pyplot as plt
from game import *
import utils


# Metrics model, which only looks at heuristic scoring metrics used for labeling
metrics_model = Sequential()
metrics_model.add(Dense(32, activation='relu', input_dim=10)) 
metrics_model.add(Dense(16, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))

# output is passed to relu() because labels are binary
metrics_model.add(Dense(1, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))
metrics_model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=["acc"])

start_board = Board()
boards_list = utils.generate_next(start_board)
branching_position = 0
nmbr_generated_game = 10000
while len(boards_list) < nmbr_generated_game:
	temp = len(boards_list) - 1
	for i in range(branching_position, len(boards_list)):
		if (utils.possible_moves(utils.reverse(utils.expand(boards_list[i]))) > 0):
				boards_list = np.vstack((boards_list, utils.generate_next(utils.reverse(utils.expand(boards_list[i])))))
	branching_position = temp

# calculate/save heuristic metrics for each game state
metrics	= np.zeros((0, 10))
winning = np.zeros((0, 1))

for board in boards_list[:nmbr_generated_game]:
	temp = utils.get_metrics(board)
	metrics = np.vstack((metrics, temp[1:]))
	winning  = np.vstack((winning, temp[0]))
 
# fit the metrics model
history = metrics_model.fit(metrics , winning, epochs=32, batch_size=64, verbose=0)

# History for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

# History for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

# Board model
board_model = Sequential()

# input dimensions is 32 board position values
board_model.add(Dense(64 , activation='relu', input_dim=32))

# use regularizers, to prevent fitting noisy labels
board_model.add(Dense(32 , activation='relu', kernel_regularizer=regularizers.l2(0.01)))
board_model.add(Dense(16 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 16
board_model.add(Dense(8 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 8

# output isn't squashed, because it might lose information
board_model.add(Dense(1 , activation='linear', kernel_regularizer=regularizers.l2(0.01)))
board_model.compile(optimizer='nadam', loss='binary_crossentropy')

# calculate heuristic metric for data
metrics = np.zeros((0, 10))
winning = np.zeros((0, 1))
data = boards_list

for board in data:
	temp = utils.get_metrics(board)
	metrics = np.vstack((metrics, temp[1:]))
	winning = np.zeros((0, 1))
 
# calculate probilistic (noisy) labels
probabilistic = metrics_model.predict_on_batch(metrics)

# fit labels to {-1, 1}
probabilistic = np.sign(probabilistic)

# calculate confidence score for each probabilistic label using error between probabilistic and weak label
confidence = 1/(1 + np.absolute(winning - probabilistic[:, 0]))
 
# pass to the Board model
board_model.fit(data, probabilistic, epochs=32, batch_size=64, sample_weight=confidence, verbose=0)

board_json = board_model.to_json()
with open('board_model.json', 'w') as json_file:
	json_file.write(board_json)
board_model.save_weights('board_model.h5')

print('Checkers Board Model saved to: board_model.json/h5')