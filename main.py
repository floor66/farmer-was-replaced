# What to harvest?
G_item_to_harvest = Items.Power
G_secondary_item = Items.Carrot

# Declare global variables
def declare_global_variables():
	current_direction = North
	world_size = get_world_size()
	plot_count = world_size*world_size
	pumpkin_count = 0
	sunflower_count = 0
	initial_lap_done = False
	poly_plot = []
	sunflower_sizes = []
	
	for _ in range(plot_count):
		sunflower_sizes.append(-1)	
		poly_plot.append(None)
	
	return current_direction, world_size, plot_count, pumpkin_count, sunflower_count, initial_lap_done, sunflower_sizes, poly_plot

G_current_direction, G_world_size, G_plot_count, G_pumpkin_count, G_sunflower_count, G_initial_lap_done, G_sunflower_sizes, G_poly_plot = declare_global_variables()	

# moveTo(0, 0)
clear()

while True:
	G_world_size = get_world_size()
	G_plot_count = G_world_size*G_world_size
	G_entity_type = get_entity_type()
	
	def coords_to_idx(x, y):
		return (x * G_world_size) + y
		
	def idx_to_coords(idx):
		return (idx // G_world_size, idx % G_world_size)
	
	G_pos_x, G_pos_y, G_idx = get_pos()
	
	if (not G_initial_lap_done) and (G_idx == (G_plot_count - 1)):
		G_initial_lap_done = True
	
	if G_item_to_harvest == Items.Power and G_sunflower_count == G_plot_count:
		sf_x, sf_y = idx_to_coords(largest_sunflower_idx())
		moveTo(sf_x, sf_y)
		G_pos_x = sf_x
		G_pos_y = sf_y
		G_idx = coords_to_idx(G_pos_x, G_pos_y)
		_, G_sunflower_count, G_sunflower_sizes = sunflower_harvest()
	elif can_harvest():
		if G_item_to_harvest == Items.Pumpkin:
			if G_entity_type == Entities.Pumpkin:
				G_pumpkin_count += 1
			if G_pumpkin_count == G_plot_count:
				harvest()
		else:
			if G_secondary_item == Items.Power:
				if G_entity_type == Entities.Sunflower:
					if G_initial_lap_done and (measure() >= max(G_sunflower_sizes)):
						_, G_sunflower_count, G_sunflower_sizes = sunflower_harvest()
				else:
					harvest()
			elif G_item_to_harvest != Items.Gold:
				harvest()

	G_entity_type = get_entity_type()
	G_ground_type = get_ground_type()
	
	if G_pos_x == 0 and G_pos_y == 0:
		G_pumpkin_count = 0
		
	if G_item_to_harvest != Items.Gold and num_items(Items.Water_Tank) > 500:
		if get_water() < 0.50:
			while get_water() < 1.0:
				use_item(Items.Water_Tank)
				
	if G_item_to_harvest == Items.Wood:
		wood()
	elif G_item_to_harvest == Items.Carrot:
		if not carrots():
			pass
	elif G_item_to_harvest == Items.Pumpkin:
		if not pumpkins():
			pass
	elif G_item_to_harvest == Items.Power:
		if not sunflowers():
			pass
	elif G_item_to_harvest == Items.Gold:
		if not maze():
			break
	
	G_entity_type = get_entity_type()
	if G_entity_type == Entities.Sunflower:
		G_sunflower_count += 1
		G_sunflower_sizes[G_idx] = measure()
		
	G_current_direction = move_()
