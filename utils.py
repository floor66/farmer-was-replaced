def coords_to_idx(x, y):
	return (x * G_world_size) + y
		
def idx_to_coords(idx):
	return (idx // G_world_size, idx % G_world_size)

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
	return 1000000000000 * (G_world_size*G_world_size)

def move_():
	new_direction = G_current_direction
	
	if G_current_direction == North:
		dir_change = G_pos_y == (G_world_size - 1)
	elif G_current_direction == South:
		dir_change = G_pos_y == 0
	
	if dir_change:
		move(East)
		
		if G_current_direction == North:
			new_direction = South
		elif G_current_direction == South:
			new_direction = North
	
	if G_current_direction == new_direction:
		move(G_current_direction)
	
	return new_direction

# Brute force/simple moving
# Doesnt keep in mind wrapping around etc
def moveTo(dest_x, dest_y):
	moves = []
	
	diff_x = dest_x - G_pos_x
	dir = East
	if diff_x < 0:
		dir = West
	for i in range(abs(diff_x)):
		moves.insert(i, dir)
	
	diff_y = dest_y - G_pos_y
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
	
	for i in range(len(G_sunflower_sizes)):
		if G_sunflower_sizes[i] > largest:
			largest = G_sunflower_sizes[i]
			largest_idx = i
	
	return largest_idx
