import numpy as np
import os
import time
import sys
from matplotlib import pyplot as plt

BOX_SIZE = 3
NUM_BOXES = 9

def box2coord(box):
	return BOX_SIZE*(box/BOX_SIZE), BOX_SIZE*(box%BOX_SIZE)

def pick_random_box():
	return np.random.randint(0, NUM_BOXES)

class Sudoku:

	T = 0.1

	def __init__(self, fname='sample1.csv'):
		self.board = np.loadtxt(fname,delimiter=',',dtype=int)
		self.board_initial = self.board == 0
		self.fname = fname
		self.print_board()

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

	def compute_energy(self, board):
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

	def solve(self, nitr=100):

		tstart = time.time()
		# do stuff
		

		self.fill_initial()

		E_hist = []

		for i in np.arange(0,nitr):
			E = self.compute_energy(self.board)
			E_hist.append(E)

			box = pick_random_box()
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

		t_elapsed = time.time() - tstart

		print 'Solved in ' + str(round(t_elapsed,3)) +' seconds.'
		self.print_board()

		#plt.plot(E_hist)

		# save
		f, ext = os.path.splitext(self.fname)
		fname_sol = f+'_sol'+ext
		np.savetxt(fname_sol, self.board, delimiter=',')
		print 'Solution saved in ' + fname_sol










