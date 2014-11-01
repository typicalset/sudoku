import numpy as np
from matplotlib import pyplot as plt

class Sudoku:

	BOX_SIZE = 3
	NUM_BOXES = 9

	T = 0.1

	def __init__(self, game_file='sample1.csv'):
		self.board = np.loadtxt(game_file,delimiter=',',dtype=int)
		self.board_initial = self.board == 0
		print self.board
		print self.board_initial

	def box2coord(self, box):
		return self.BOX_SIZE*(box/self.BOX_SIZE), self.BOX_SIZE*(box%self.BOX_SIZE)

	def find_missing_numbers(self,x,y):
		missing_numbers = []
		for i in np.arange(1,self.NUM_BOXES+1):
			if i not in self.board[x:x+self.BOX_SIZE,y:y+self.BOX_SIZE]:
				missing_numbers.append(i)

		return missing_numbers

	def fill_box(self, box):
		x,y = self.box2coord(box)

		missing_numbers = self.find_missing_numbers(x,y)
		np.random.shuffle(missing_numbers)
		
		missing_x, missing_y = np.where(self.board[x:x+self.BOX_SIZE,y:y+self.BOX_SIZE] == 0)

		self.board[x+missing_x, y+missing_y] = missing_numbers

	def fill_initial(self):
		for i in np.arange(0, self.NUM_BOXES):
			self.fill_box(i)

	def count_duplicates(self, board):
		num_duplicates = 0
		for i in np.arange(0,self.NUM_BOXES):
			num_duplicates += 2*self.NUM_BOXES - len(np.unique(board[i,:])) - len(np.unique(board[:,i]))
		return num_duplicates

	def compute_energy(self, board):
		#return 2*self.NUM_BOXES*self.NUM_BOXES - self.count_duplicates(board)
		return self.count_duplicates(board)

	def pick_random_box(self):
		return np.random.randint(0, self.NUM_BOXES)

	def swap_squares(self, square1, square2):
		self.board[square1], self.board[square2] = self.board[square2], self.board[square1]

	def propose_swap(self, box):
		x,y = self.box2coord(box)
		swappable_x, swappable_y = np.where(self.board_initial[x:x+self.BOX_SIZE,y:y+self.BOX_SIZE])

		# randomly pick two squares to swap
		i,j = tuple(np.random.choice(len(swappable_x), 2, replace=False))

		square1 = x+swappable_x[i], y+swappable_y[i]
		square2 = x+swappable_x[j], y+swappable_y[j]

		return square1, square2


	# quick and dirty method for checking completion
	def is_done(self):
		return (np.sum(self.board, 0) == np.sum(self.board,1)).all()

	def solve(self, nitr=100):
		self.fill_initial()


		E_hist = []

		for i in np.arange(0,nitr):
			E = self.compute_energy(self.board)
			E_hist.append(E)

			box = self.pick_random_box()
			square1, square2 = self.propose_swap(box)
			self.swap_squares(square1, square2)
			E_proposal = self.compute_energy(self.board)

			if E_proposal >= E:
				if np.exp(-(E_proposal-E)/self.T) < np.random.random():
					self.swap_squares(square1, square2)
				else:
					pass # accept proposal
			else:
				pass # accept proposal

		plt.plot(E_hist)
		return E_hist










