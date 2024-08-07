globals = {
	"world_size": get_world_size(),
	"current_direction": North,
	"plot_count": get_world_size() * get_world_size(),
	"crop_counts": {
		"pumpkin": 0,
		"sunflower": 0
	},
	"initial_lap_completed": False,
	"use_poly": False,
	"poly_plot": {},
	"sunflower_sizes": [],
	"cactus_sizes": {},
	"pos_x": get_pos_x(),
	"pos_y": get_pos_y(),
	"infinity": 1000000000000 * (get_world_size() * get_world_size()),
	"item_to_harvest": None,
	"secondary_item": None
}

globals["pos_idx"] = coords_to_idx(globals["pos_x"], globals["pos_y"])
globals["sunflower_sizes"] = init_list(globals["plot_count"], -1)

# Harvesting checks
def do_harvest():
	if globals["item_to_harvest"] == Items.Power and globals["crop_counts"]["sunflower"] == globals["plot_count"]:
		move_to_idx(largest_sunflower_idx())
		sunflower_harvest()
	elif globals["item_to_harvest"] == Items.Cactus:
		if globals["initial_lap_completed"]:
			harvest()
			move_to_idx(0)
			globals["initial_lap_completed"] = False
			globals["cactus_sizes"] = {}
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

def loop(goal_fn):
	while not goal_fn():
		if globals["item_to_harvest"] == Items.Gold:
			if maze(299, [solve_bfs], ["bfs_rec"]):
				harvest()
			return

		globals["world_size"] = get_world_size()
		globals["plot_count"] = globals["world_size"] * globals["world_size"]
		globals["entity_type"] = get_entity_type()
		globals["pos_x"], globals["pos_y"], globals["pos_idx"] = get_pos()

		do_harvest()

		# Check entity type again as we could have harvested
		globals["entity_type"] = get_entity_type()
		globals["ground_type"] = get_ground_type()
		
		# We re-count pumpkins every lap
		if globals["pos_x"] == 0 and globals["pos_y"] == 0:
			globals["crop_counts"]["pumpkin"] = 0
		
		watering()
		planting()
		
		# Check entity type again as we could have planted
		globals["entity_type"] = get_entity_type()
		if globals["entity_type"] == Entities.Sunflower:
			globals["crop_counts"]["sunflower"] += 1
			globals["sunflower_sizes"][globals["pos_idx"]] = measure()
			
		if (not globals["initial_lap_completed"]) and (globals["pos_idx"] == globals["plot_count"] - 1):
			globals["initial_lap_completed"] = True
		
		next_idx = globals["pos_idx"] + 1
		if next_idx > globals["plot_count"] - 1:
			next_idx = 0
		move_to_idx(next_idx)

def main():
	# set_execution_speed(3)
	# clear()
	# globals["pos_x"], globals["pos_y"], globals["pos_idx"] = get_pos()
	# move_to_coords(0, 9)
	# move_to_coords(1, 0)
	run_default_strategy()

# Entry point
main()
