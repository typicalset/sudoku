import numpy as np
import os
import time
import sys
from matplotlib import pyplot as plt

BOX_SIZE = 3
NUM_BOXES = 9

def check_board(board):
	if board.shape != (NUM_BOXES,NUM_BOXES):
		raise Exception("Board is of wrong dimensions!")
	if (board<0).any() or (board>=(NUM_BOXES+1)).any():
		raise Exception("Numbers must be integers between 1 and 9!")

def box2coord(box):
	return BOX_SIZE*(box/BOX_SIZE), BOX_SIZE*(box%BOX_SIZE)

def pick_random_box():
	return np.random.randint(0, NUM_BOXES)

class Sudoku:

	def __init__(self, fname='sample1.csv'):
		self.load_board(fname)

	def load_board(self, fname):
		self.board = np.loadtxt(fname,delimiter=',',dtype=int)
		check_board(self.board)
		self.board_initial = self.board == 0
		self.fname = fname
		self.print_board()
		print 'Squares to fill: ' + str(sum(sum(self.board_initial)))

	def find_missing_numbers(self,x,y):
		missing_numbers = []
		for i in np.arange(1,NUM_BOXES+1):
			if i not in self.board[x:x+BOX_SIZE,y:y+BOX_SIZE]:
				missing_numbers.append(i)

		return missing_numbers

	def fill_box(self, box):
		x,y = box2coord(box)

		missing_numbers = self.find_missing_numbers(x,y)
		np.random.shuffle(missing_numbers)
		
		missing_x, missing_y = np.where(self.board[x:x+BOX_SIZE,y:y+BOX_SIZE] == 0)

		self.board[x+missing_x, y+missing_y] = missing_numbers

	def fill_initial(self):
		for i in np.arange(0, NUM_BOXES):
			self.fill_box(i)

	def compute_energy(self):
		num_duplicates = 0
		for i in np.arange(0, NUM_BOXES):
			num_duplicates += 2*NUM_BOXES - len(np.unique(self.board[i,:])) - len(np.unique(self.board[:,i]))
		return num_duplicates

	def swap_squares(self, square1, square2):
		self.board[square1], self.board[square2] = self.board[square2], self.board[square1]

	def propose_swap(self, box):
		x,y = box2coord(box)
		swappable_x, swappable_y = np.where(self.board_initial[x:x+BOX_SIZE,y:y+BOX_SIZE])

		# randomly pick two squares to swap
		i,j = tuple(np.random.choice(len(swappable_x), 2, replace=False))

		square1 = x+swappable_x[i], y+swappable_y[i]
		square2 = x+swappable_x[j], y+swappable_y[j]

		return square1, square2

	# quick and dirty method for checking completion
	def is_done(self):
		return (np.sum(self.board, 0) == np.sum(self.board,1)).all()

	# print the sudoku board in a user friendly format
	def print_board(self):
		print ''
		for i in np.arange(0,NUM_BOXES):
			if i!= 0 and i%3 == 0:
				sys.stdout.write((2*(NUM_BOXES)+3)*'-'+'\n')
			for j in np.arange(0,NUM_BOXES):
				if j != 0 and j%3 == 0:
					sys.stdout.write('| ')
				sys.stdout.write(str(self.board[i,j]) + ' ')
			sys.stdout.write('\n')
		print ''

	def solve(self):

		# these parameters were tuned
		T = 2.0
		cooling_interval = 500
		cooling_rate = 0.9
		reheat_level = 0.05
		T_reheat = 0.5

		tstart = time.time()

		self.fill_initial()

		E_hist = []
		deltaE_hist = []

		num_rejects = 0

		nitr = 0

		while True:
			E = self.compute_energy()
			if E == 0:
				# we're done
				break
			E_hist.append(E)

			box = pick_random_box()
			square1, square2 = self.propose_swap(box)
			self.swap_squares(square1, square2)
			E_proposal = self.compute_energy()

			deltaE = E_proposal-E
			deltaE_hist.append(deltaE)

			if np.random.rand() < np.exp(-deltaE/T):
				# accept
				pass
			else:
				# reject, revert back to old configuration
				self.swap_squares(square1, square2)

			if nitr % cooling_interval == 0:
				T = T*cooling_rate
				# "barrier avoidance" - avoid settling into local minima
				if (T < reheat_level):
					T = T_reheat

			nitr += 1
			if nitr % 20000 == 0:
				t_elapsed = time.time() - tstart
				print str(round(t_elapsed,0)) +' seconds...'

		t_elapsed = time.time() - tstart
		print ' ' + str(round(t_elapsed,3)) +' seconds.'

		print 'Solved in ' + str(round(t_elapsed,3)) +' seconds.'
		self.print_board()

		plt.plot(E_hist)
		plt.xlabel('iteration')
		plt.ylabel('Energy')

		# save
		f, ext = os.path.splitext(self.fname)
		fname_sol = f+'_sol'+ext
		np.savetxt(fname_sol, self.board, delimiter=',', fmt='%d')
		print 'Solution saved in ' + fname_sol
