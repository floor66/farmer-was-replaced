def wood():
	if globals["pos_y"] % 2 == 0 and globals["pos_x"] % 2 == 0:
		plant(Entities.Tree)
	else:
		if globals["secondary_item"] == Items.Wood:
			plant(Entities.Bush)
		elif globals["secondary_item"] == Items.Hay:
			pass
		elif globals["secondary_item"] == Items.Carrot:
			carrots()
		elif globals["secondary_item"] == Items.Power:
			sunflowers()
		else:
			rnd = random()
			if rnd <= 0.25:
				plant(Entities.Bush)
			elif rnd > 0.25 and rnd <= 0.50:
				carrots()
			elif rnd > 0.50:
				pass
	
	return True

def sunflowers():
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

def carrots():
	if num_items(Items.Carrot_Seed) == 0:
		if not trade(Items.Carrot_Seed):
			return False
		
	if globals["ground_type"] != Grounds.Soil:
		till()
	
	if globals["entity_type"] != Entities.Carrots:
		plant(Entities.Carrots)
	
	return True

def pumpkins():
	if num_items(Items.Pumpkin_Seed) == 0:
		if not trade(Items.Pumpkin_Seed):
			return False
		
	if globals["ground_type"] != Grounds.Soil:
		till()
		
	if globals["entity_type"] != Entities.Pumpkin:
		plant(Entities.Pumpkin)

def fertilize(do_wait=True):
	if num_items(Items.Fertilizer) == 0:
		if not trade(Items.Fertilizer):
			if do_wait:
				while True:
					if can_harvest():
						return
			else:
				return False

	use_item(Items.Fertilizer)	
	return True
