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

def move_to_next_plot():
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
def move_to_coords(dest_x, dest_y, force_update_pos=False, wrap_around=True):
	if force_update_pos:
		globals["pos_x"], globals["pos_y"], globals["pos_idx"] = get_pos()
	
	diff_x, diff_y = dest_x - globals["pos_x"], dest_y - globals["pos_y"]
	
	# if we need to move more than half of the board, go the opposite way
	dirs = {-1: West, 1: East}
	while globals["pos_x"] != dest_x:
		sign = diff_x / abs(diff_x)
		if wrap_around and abs(diff_x) > ((globals["world_size"] - 1) // 2):
			sign = -sign
		move(dirs[sign])

		if wrap_around:
			if globals["pos_x"] == globals["world_size"] - 1 and dirs[sign] == East:
				globals["pos_x"] = 0
			elif globals["pos_x"] == 0 and dirs[sign] == West:
				globals["pos_x"] = globals["world_size"] - 1
			else:
				globals["pos_x"] += sign
		else:
			globals["pos_x"] += sign
	
	dirs = {-1: South, 1: North}
	while globals["pos_y"] != dest_y:
		sign = diff_y / abs(diff_y)
		if wrap_around and abs(diff_y) > ((globals["world_size"] - 1) // 2):
			sign = -sign
		move(dirs[sign])

		if wrap_around:
			if globals["pos_y"] == globals["world_size"] - 1 and dirs[sign] == North:
				globals["pos_y"] = 0
			elif globals["pos_y"] == 0 and dirs[sign] == South:
				globals["pos_y"] = globals["world_size"] - 1
			else:
				globals["pos_y"] += sign
		else:
			globals["pos_y"] += sign

	globals["pos_idx"] = coords_to_idx(globals["pos_x"], globals["pos_y"])

def move_to_idx(idx, force_update_pos=False, wrap_around=True):
	x, y = idx_to_coords(idx)
	move_to_coords(x, y, force_update_pos, wrap_around)

def move_to_next_idx():
	next_idx = globals["pos_idx"] + 1
	if next_idx > globals["plot_count"] - 1:
		next_idx = 0
	move_to_idx(next_idx)
	
def largest_sunflower_idx():
	largest = -1
	largest_idx = -1
	
	for i in range(len(globals["sunflower_sizes"])):
		if globals["sunflower_sizes"][i] > largest:
			largest = globals["sunflower_sizes"][i]
			largest_idx = i
	
	return largest_idx

def greedy_sort(L):
	result = []

	for i in range(len(L)):
		c = len(result)

		for j in range(len(result)):
			if L[i] < result[j]:
				c = j
				break

		result.insert(c, L[i])
			
	return result

def sum(L):
	c = 0
	for a in L:
		c += a
	return c

def mean(L):
	if len(L) == 0:
		return None
	
	return sum(L) / len(L)

def median(L):
	L_sorted = greedy_sort(L)
	L_sorted_len = len(L_sorted)
	middle = L_sorted_len // 2

	if L_sorted_len % 2 == 1:
		return L_sorted[middle]
	else:
		return (L_sorted[middle - 1] + L_sorted[middle]) / 2
	