import numpy as np
import matplotlib.pyplot as plot
from keras.models import model_from_json
import json
from board import *
from utils import *

json_file = open('board_model.json', 'r')
board_json = json_file.read()
json_file.close()

reinforced_model = model_from_json(board_json)
reinforced_model.load_weights('board_model.h5')
reinforced_model.compile(optimizer='adadelta', loss='mean_squared_error')

data = np.zeros((1, 32))
labels = np.zeros(1)
win = lose = draw = 0
winrates = []
learning_rate = 0.5
discount_factor = 0.95

for gen in range(0, 500):
	for game in range(0, 200):
		temp_data = np.zeros((1, 32))
		board = Board()
		player = np.sign(np.random.random() - 0.5)
		turn = 0
		while (True):
			moved = False
			boards = np.zeros((0, 32))
			if (player == 1):
				board = generate_next(board)
			else:
				boards = generate_next(reverse(board))

			scores = reinforced_model.predict_on_batch(boards)
			max_index = np.argmax(scores)
			best = boards[max_index]

			if (player == 1):
				board = expand(best)
				temp_data = np.vstack((temp_data, compress(board)))
			else:
				board = reverse(expand(best))

			player = -player

			# punish losing games, reward winners  & drawish games reaching more than 200 turns
			winner = board.winner()
			if (winner == 1 or (winner == 0 and turn >= 200) ):
				if winner == 1:
					win = win + 1
				else:
					draw = draw + 1
				reward = 10
				old_prediction = reinforced_model.predict_on_batch(temp_data[1:])
				optimal_futur_value = np.ones(old_prediction.shape)
				temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction ) # Q-Learning
				data = np.vstack((data, temp_data[1:]))
				labels = np.vstack((labels, temp_labels))
				break
			elif (winner == -1):
				lose = lose + 1
				reward = -10
				old_prediction = reinforced_model.predict_on_batch(temp_data[1:])
				optimal_futur_value = -1*np.ones(old_prediction.shape)
				temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
				data = np.vstack((data, temp_data[1:]))
				labels = np.vstack((labels, temp_labels))
				break
			turn = turn + 1

		if ((game+1) % 200 == 0):
			reinforced_model.fit(data[1:], labels[1:], epochs=16, batch_size=256, verbose=0)
			data = np.zeros((1, 32))
			labels = np.zeros(1)
	winrate = int((win+draw)/(win+draw+lose)*100)
	winrates.append(winrate)
 
	reinforced_model.save_weights('reinforced_model.h5')
 
print('Checkers Board Model updated by reinforcement learning & saved to: reinforced_model.json/h5')

generations = range(0, 500)
print("Final win/draw rate : " + str(winrates[499])+"%" )
plot.plot(generations,winrates)
plot.show()