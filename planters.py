def hay():
	if globals["ground_type"] != Grounds.Turf:
		till()

	return True

def bush():
	if globals["ground_type"] != Grounds.Turf:
		till()

	plant(Entities.Bush)
	return True

def tree():
	if globals["pos_y"] % 2 == 0 and globals["pos_x"] % 2 == 0:
		plant(Entities.Tree)
	elif not globals["use_poly"]:
		if globals["secondary_item"] == Items.Wood:
			bush()
		elif globals["secondary_item"] == Items.Hay:
			pass
		elif globals["secondary_item"] == Items.Carrot:
			carrot()
		elif globals["secondary_item"] == Items.Power:
			sunflower()
	
	return True

def sunflower():
	if num_items(Items.Sunflower_Seed) == 0:
		if not trade(Items.Sunflower_Seed):
			return False
	
	if globals["ground_type"] != Grounds.Soil:
		till()
	
	if globals["entity_type"] != Entities.Sunflower:
		plant(Entities.Sunflower)
	
	return True

def sunflower_harvest():
	if not can_harvest():
		if not fertilize():
			return False
	harvest()
	
	globals["sunflower_sizes"][globals["pos_idx"]] = -1
	globals["crop_counts"]["sunflower"] -= 1
	
	return True

def carrot():
	if num_items(Items.Carrot_Seed) == 0:
		if not trade(Items.Carrot_Seed):
			return False
		
	if globals["ground_type"] != Grounds.Soil:
		till()
	
	if globals["entity_type"] != Entities.Carrots:
		plant(Entities.Carrots)
	
	return True

def pumpkin():
	if num_items(Items.Pumpkin_Seed) == 0:
		if not trade(Items.Pumpkin_Seed):
			return False
		
	if globals["ground_type"] != Grounds.Soil:
		till()
		
	if globals["entity_type"] != Entities.Pumpkin:
		plant(Entities.Pumpkin)

	return True

# Tries to fertilize the current plot
# do_wait determines whether to wait for the crop to grow in case we can't buy fertilizer
def fertilize(do_wait=True):
	if num_items(Items.Fertilizer) == 0:
		if not trade(Items.Fertilizer):
			if do_wait:
				while True:
					if can_harvest():
						return True
			else:
				return False

	use_item(Items.Fertilizer)	
	return True

def cactus():
	if num_items(Items.Cactus_Seed) == 0:
		if not trade(Items.Cactus_Seed):
			return False
	
	if globals["ground_type"] != Grounds.Soil:
		till()
		
	if globals["entity_type"] != Entities.Cactus:
		plant(Entities.Cactus)

	start_idx = globals["pos_idx"]
	globals["cactus_sizes"][start_idx] = measure()
	
	# Cacti should be <= South and West
	#                 >= North and East
	for idx in range(start_idx, -1, -1):
		curr_size = globals["cactus_sizes"][idx]
		cx, cy = idx_to_coords(idx)

		neighbors = {
			North: {"constraint": cy < globals["world_size"] - 1, "coords": (0, 1), "compare_direction": 1},
			East: {"constraint": cx < globals["world_size"] - 1, "coords": (1, 0), "compare_direction": 1},
			South: {"constraint": cy > 0, "coords": (0, -1), "compare_direction": -1},
			West: {"constraint": cx > 0, "coords": (-1, 0), "compare_direction": -1},
		}

		for dir in neighbors:
			dir_idx = coords_to_idx(cx + neighbors[dir]["coords"][0], cy + neighbors[dir]["coords"][1])
			if not (dir_idx in globals["cactus_sizes"]) or not neighbors[dir]["constraint"]:
				continue
			
			if (curr_size * neighbors[dir]["compare_direction"]) > (globals["cactus_sizes"][dir_idx] * neighbors[dir]["compare_direction"]):
				move_to_idx(idx)
				swap(dir)
				globals["cactus_sizes"][idx] = globals["cactus_sizes"][dir_idx]
				globals["cactus_sizes"][dir_idx] = curr_size
				break
	move_to_idx(start_idx)

	return True

def dino():
	if num_items(Items.Egg) == 0:
		if not trade(Items.Egg):
			return False

	use_item(Items.Egg)	
	return True