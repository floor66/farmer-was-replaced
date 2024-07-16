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
# Doesnt keep in mind wrapping around etc because maze doesnt allow it (I think?)
def moveTo(dest_x, dest_y, force_update_pos=False):
	if force_update_pos:
		globals["pos_x"], globals["pos_y"], globals["pos_idx"] = get_pos()
	
	diff_x, diff_y = dest_x - globals["pos_x"], dest_y - globals["pos_y"]

	dirs = {-1: West, 1: East}
	while diff_x != 0:
		sign = diff_x / abs(diff_x)
		move(dirs[sign])
		globals["pos_x"] += sign
		diff_x = dest_x - globals["pos_x"]
	
	dirs = {-1: South, 1: North}
	while diff_y != 0:
		sign = diff_y / abs(diff_y)
		move(dirs[sign])
		globals["pos_y"] += sign
		diff_y = dest_y - globals["pos_y"]


def largest_sunflower_idx():
	largest = -1
	largest_idx = -1
	
	for i in range(len(globals["sunflower_sizes"])):
		if globals["sunflower_sizes"][i] > largest:
			largest = globals["sunflower_sizes"][i]
			largest_idx = i
	
	return largest_idx
