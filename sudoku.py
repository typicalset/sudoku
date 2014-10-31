import numpy as np

class Sudoku:

	BOX_SIZE = 3
	NUM_BOXES = 9


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


	def pick_random_box(self):
		return np.random.randint(0, self.NUM_BOXES)


	def swap_squares(self, box):
		x,y = self.box2coord(box)
		swappable_x, swappable_y = np.where(self.board_initial[x:x+self.BOX_SIZE,y:y+self.BOX_SIZE])

		# randomly pick two squares to swap
		# make the swap


	# quick and dirty method for checking completion
	def is_done(self):
		return (np.sum(self.board, 0) == np.sum(self.board,1)).all()

	def solve(self):
		self.fill_initial()








