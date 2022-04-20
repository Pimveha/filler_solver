import random as r
import itertools
from json import dumps

class Filler_check():
	# def __init__(self, board, capt_pos = [(6,0)]):
	def __init__(self, board, capt_pos):
		self.board = board
		self.capt_pos = capt_pos
		self.neighbors = None
		self.neighbors_color_pos_dict = None

	def get_capt_pos(self):
		return self.capt_pos

	def gen_neighbors(self):
		neighbors = []
		for i in range(len(self.capt_pos)):
			y, x = self.capt_pos[i]
			neighbors.append((y-1,x))
			neighbors.append((y+1,x))
			neighbors.append((y,x-1))
			neighbors.append((y,x+1))
			# neighbors.extend(zip((y-1,x), (y+1,x), (y,x-1), (y,x+1)))

		# clean up neighbors
		neighbors_to_remove = []
		for i in range(len(neighbors)-1):
			y, x = neighbors[i]
			if neighbors[i] in self.capt_pos:
				neighbors_to_remove.append(neighbors[i])
			elif x < 0:
				neighbors_to_remove.append(neighbors[i])
			elif y < 0:
				neighbors_to_remove.append(neighbors[i])
			elif y > len(self.board)-1:
				neighbors_to_remove.append(neighbors[i])
			elif x > len(self.board[0])-1:
				neighbors_to_remove.append(neighbors[i])
		for i in range(len(neighbors_to_remove)):
			if neighbors_to_remove[i] in neighbors:
				neighbors.remove(neighbors_to_remove[i])
		self.neighbors = neighbors
		# return neighbors

	def get_neighbors(self):
		return self.neighbors

	def get_neighbor_colors(self):
		neighbors_color_pos_dict = {}
		for i in range(len(self.neighbors)):
			y, x = self.neighbors[i]
			if self.board[y][x] in neighbors_color_pos_dict.keys():
				neighbors_color_pos_dict[self.board[y][x]].append(self.neighbors[i])
			else:
				neighbors_color_pos_dict[self.board[y][x]] = [self.neighbors[i]]
		self.neighbors_color_pos_dict = neighbors_color_pos_dict
		# return neighbors_color_pos_dict
	def get_neighbors_color_pos_dict(self):
		return self.neighbors_color_pos_dict

	def enlarge_through_color(self, itt_color):
		# print(self.neighbors_color_pos_dict.items())
		if itt_color in self.neighbors_color_pos_dict.keys():
			list_to_add = self.neighbors_color_pos_dict[itt_color]
			for i in range(len(list_to_add)):
				self.capt_pos.append(list_to_add[i])
		else:
			return f"no {itt_color} neighbors"
		return f"{len(list_to_add)} {itt_color} tile(s) added"


	def __repr__(self):
		return f"captured tiles: {self.capt_pos}"




def gen_board():
	boards_x = 8
	boards_y = 7
	board = []
	for i in range(boards_y+1):
		x_list = ["o" for i in range(boards_x+1)]
		board.append(x_list)
	col_list = ["prp", "blk", "blu", "yel", "red", "grn"]
	for i in range(len(board)-1):
		for j in range(len(board[i])-1):
			color = r.choice(col_list)
			try:
				while color in [board[i-1][j], board[i+1][j], board[i][j-1], board[i][j+1]]:
					# print(f"{color} zat in: {[board[i-1][j], board[i+1][j], board[i][j-1], board[i][j+1]]}")
					color = r.choice(col_list)
			except IndexError:
				continue
			board[i][j] = color
	for i in range(len(board)):
		board[i] = board[i][:-1]
	board = board[:-1]
	return board

def gen_itter(depth):
	col_list = ["prp", "blk", "blu", "yel", "red", "grn"]
	itt1 = list(itertools.product(col_list, repeat = depth))
	list_to_remove = []
	for i in range(len(itt1)):
		for j in range(depth-1):
			if itt1[i][j] == itt1[i][j+1]:
				list_to_remove.append(itt1[i])

	for i in range(len(list_to_remove)):
		if list_to_remove[i] in itt1:
			itt1.remove(list_to_remove[i])
	return itt1

def pretty_print(board):
	for i in range(len(board)):
		print(board[i])

def class_dict(board, itt, depth, capt_pos):
	itt_res_dict = {}
	for i in range(len(itt)):
		itt_res_dict[itt[i]] = Filler_check(board, capt_pos[:])

		for j in range(depth):
			# print(itt_res_dict[itt[i]].gen_neighbors())
			# print(itt_res_dict[itt[i]].get_neighbors())
			# print(itt_res_dict[itt[i]].get_neighbor_colors())
			# print(itt_res_dict[itt[i]].enlarge_through_color(itt[i][j]))
			# print(itt_res_dict[itt[i]].get_capt_pos())

			itt_res_dict[itt[i]].gen_neighbors()
			itt_res_dict[itt[i]].get_neighbors()
			itt_res_dict[itt[i]].get_neighbor_colors()
			itt_res_dict[itt[i]].enlarge_through_color(itt[i][j])
			itt_res_dict[itt[i]].get_capt_pos()


	# print(itt_res_dict)

	# sorted dict
	num_dict = {}

	for i in range(len(itt_res_dict)):
		num_dict[str(itt[i])] = len(itt_res_dict[itt[i]].get_capt_pos()), f"{itt_res_dict[itt[i]].get_capt_pos()}"

	a = sorted(num_dict.items(), key=lambda x: x[1])
	sorted_dict = {k: v for k, v in a}
	# print(sorted_dict)
	# print(type(sorted_dict))
	pretty = dumps(sorted_dict, indent=4)
	# print(pretty)

	print("--------")
	print("top 20 best keys:")
	i = 20

	# list of best captured positions:
	best_capt_list = []


	while i > 0:
		print(list(sorted_dict.keys())[-i])
		print(f"\t{list(sorted_dict.values())[-i]}\n")
		best_capt_list.append(list(sorted_dict.values())[-i][1])
		i -= 1


	# print(best_capt_list)

	return best_capt_list



def main():

	# gen_board() can be used to generate randoma filler board

	board = [['prp', 'grn', 'red', 'grn', 'yel', 'red', 'grn', 'yel'], ['yel', 'red', 'blu', 'red', 'prp', 'blk', 'prp', 'red'], ['grn', 'blu', 'blk', 'prp', 'blu', 'prp', 'red', 'blk'], ['blu', 'yel', 'grn', 'blk', 'yel', 'grn', 'blu', 'red'], ['red', 'prp', 'blu', 'red', 'prp', 'blk', 'yel', 'blu'], ['blk', 'grn', 'red', 'blk', 'yel', 'blu', 'grn', 'prp'], ['prp', 'blu', 'prp', 'yel', 'prp', 'blk', 'prp', 'blk']]
	pretty_print(board)

	# change the depth of your search, depth above 6 will take a long time, because my search method is very primative
	depth = 4
	itt = gen_itter(depth)

	# change the capt_pos if you want to search through the board wherein you've alreachy captuerd tiles. 
	capt_pos = [(6,0)]
	# capt_pos = [(6, 0), (6, 1), (5, 0), (5, 1), (5, 1), (4, 0), (5, 2), (5, 2), (6, 2), (4, 1), (4, 1), (4, 1), (6, 2), (6, 2), (6, 3), (3, 1), (3, 1), (3, 1), (6, 3), (6, 3), (3, 0), (4, 2), (4, 2), (4, 2), (4, 2), (4, 2), (2, 1), (3, 0), (2, 1), (3, 0), (2, 1), (3, 0)]
	
	best_capt_list = class_dict(board, itt, depth, capt_pos)
	# print(best_capt_list) returns the top 20 capture outcomes
	# print(best_capt_list[-1]) could be used for capt_pos input for example.



if __name__ == "__main__":
	 main()









