# clear()

globals = {
	"world_size": get_world_size(),
	"current_direction": North,
	"plot_count": get_world_size() * get_world_size(),
	"crop_counts": {
		"pumpkin": 0,
		"sunflower": 0
	},
	"initial_lap_completed": False,
	"poly_plot": [],
	"sunflower_sizes": [],
	"pos_x": get_pos_x(),
	"pos_y": get_pos_y(),
}

globals["pos_idx"] = coords_to_idx(globals["pos_x"], globals["pos_y"])
globals["poly_plot"] = init_list(globals["plot_count"], None)
globals["sunflower_sizes"] = init_list(globals["plot_count"], -1)

# What to harvest?
globals["item_to_harvest"] = Items.Wood
globals["secondary_item"] = Items.Power

def main():
	def loop():
		globals["world_size"] = get_world_size()
		globals["plot_count"] = globals["world_size"] * globals["world_size"]
		globals["entity_type"] = get_entity_type()
		globals["pos_x"], globals["pos_y"], globals["pos_idx"] = get_pos()
		
		if globals["item_to_harvest"] == Items.Power and globals["crop_counts"]["sunflower"] == globals["plot_count"]:
			move_to_idx(largest_sunflower_idx())
			globals["pos_x"] = sf_x
			globals["pos_y"] = sf_y
			globals["pos_idx"] = coords_to_idx(globals["pos_x"], globals["pos_y"])
			sunflower_harvest()
		elif can_harvest():
			if globals["item_to_harvest"] == Items.Pumpkin:
				if globals["entity_type"] == Entities.Pumpkin:
					globals["crop_counts"]["pumpkin"] += 1
				if globals["crop_counts"]["pumpkin"] == globals["plot_count"]:
					harvest()
			else:
				if globals["secondary_item"] == Items.Power:
					if globals["entity_type"] == Entities.Sunflower:
						if globals["initial_lap_completed"] and (measure() >= max(globals["sunflower_sizes"])):
							sunflower_harvest()
					else:
						harvest()
				elif globals["item_to_harvest"] != Items.Gold:
					harvest()

		globals["entity_type"] = get_entity_type()
		globals["ground_type"] = get_ground_type()
		
		if globals["pos_x"] == 0 and globals["pos_y"] == 0:
			globals["crop_counts"]["pumpkin"] = 0
			
		if globals["item_to_harvest"] != Items.Gold and num_items(Items.Water_Tank) > 500:
			if get_water() < 0.50:
				while get_water() < 1.0:
					use_item(Items.Water_Tank)
					
		if globals["item_to_harvest"] == Items.Wood:
			wood()
		elif globals["item_to_harvest"] == Items.Carrot:
			if not carrots():
				pass
		elif globals["item_to_harvest"] == Items.Pumpkin:
			if not pumpkins():
				pass
		elif globals["item_to_harvest"] == Items.Power:
			if not sunflowers():
				pass
		elif globals["item_to_harvest"] == Items.Gold:
			if not maze():
				return
		
		globals["entity_type"] = get_entity_type()
		if globals["entity_type"] == Entities.Sunflower:
			globals["crop_counts"]["sunflower"] += 1
			globals["sunflower_sizes"][globals["pos_idx"]] = measure()
			
		if (not globals["initial_lap_completed"]) and (globals["pos_idx"] == (globals["plot_count"] - 1)):
			globals["initial_lap_completed"] = True
		
		globals["current_direction"] = move_to_next_plot()
	
	while True:
		loop()

# Entry point
start_count = get_op_count()
start_time = get_time()
if maze(25, [solve_bfs_it], ["bfs (it)"]):
	print(get_op_count() - start_count, "ops in", get_time() - start_time, "sec")
	# harvest()
