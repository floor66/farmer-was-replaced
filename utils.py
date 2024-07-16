def coords_to_idx(x, y):
	return (x * globals["world_size"]) + y
		
def idx_to_coords(idx):
	return (idx // globals["world_size"], idx % globals["world_size"])

def get_pos():
	pos_x = get_pos_x()
	pos_y = get_pos_y()
	return pos_x, pos_y, coords_to_idx(pos_x, pos_y)

def init_list(n, withValue=None):
	tmp_list = []
	for _ in range(n):
		tmp_list.append(withValue)
	return tmp_list

# Infinity doesnt exist in the game so we crudely implement it
def infinity():
	return 1000000000000 * (globals["world_size"]*globals["world_size"])

def move_():
	new_direction = globals["current_direction"]
	
	if globals["current_direction"] == North:
		dir_change = globals["pos_y"] == (globals["world_size"] - 1)
	elif globals["current_direction"] == South:
		dir_change = globals["pos_y"] == 0
	
	if dir_change:
		move(East)
		
		if globals["current_direction"] == North:
			new_direction = South
		elif globals["current_direction"] == South:
			new_direction = North
	
	if globals["current_direction"] == new_direction:
		move(globals["current_direction"])
	
	return new_direction

# Brute force/simple moving
# Doesnt keep in mind wrapping around etc
def moveTo(dest_x, dest_y):
	moves = []
	
	diff_x = dest_x - globals["pos_x"]
	dir = East
	if diff_x < 0:
		dir = West
	for i in range(abs(diff_x)):
		moves.insert(i, dir)
	
	diff_y = dest_y - globals["pos_y"]
	dir = North
	if diff_y < 0:
		dir = South
	for i in range(abs(diff_y)):
		moves.insert(i, dir)
	
	for m in moves:
		move(m)

def largest_sunflower_idx():
	largest = -1
	largest_idx = -1
	
	for i in range(len(globals["sunflower_sizes"])):
		if globals["sunflower_sizes"][i] > largest:
			largest = globals["sunflower_sizes"][i]
			largest_idx = i
	
	return largest_idx
