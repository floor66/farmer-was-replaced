def maze_bruteforce():
	# First, we get a maze
	plant(Entities.Bush)
	next_x, next_y = None, None
	possible_moves_all = []
	
	for _ in range(globals["plot_count"]):
		possible_moves_all.append(None)
	
	for i in range(5):
		if i > 0:
			quick_print(possible_moves_all)
			
		while get_entity_type() != Entities.Hedge:
			if not trade(Items.Fertilizer):
				print("Need fertilizer for Maze!")
				return False
			use_item(Items.Fertilizer)
	
		# Set up some variables we need	
		moves = [North, East, South, West]
		moves_performed = []
		possible_moves = []
		
		for _ in range(globals["plot_count"]):
			possible_moves.append(None)
		
		def get_opposite_move(mm):
			opposite_moves = [South, West, North, East]
			for j in range(len(moves)):
				if moves[j] == mm:
					return opposite_moves[j]
	
		# Solve the maze
		while get_entity_type() != Entities.Treasure:
			idx = coords_to_idx(get_pos_x(), get_pos_y())
			
			# Explore unknown node
			if possible_moves_all[idx] == None:
				possible_moves_all[idx] = []
				possible_moves[idx] = []

				for m in moves:
					# Probe if we can move in this direction
					if move(m):
						if get_entity_type() == Entities.Treasure:
							break
					
						possible_moves[idx].append(m)
						possible_moves_all[idx].append(m)
						move(get_opposite_move(m))
			elif possible_moves[idx] == None:
				possible_moves[idx] = []
				for m in possible_moves_all[idx]:
					possible_moves[idx].append(m)
						
			if get_entity_type() == Entities.Treasure:
				break
			
			# If all possible paths here were exhausted, backtrack
			if len(possible_moves[idx]) == 0:
				move(get_opposite_move(moves_performed.pop()))
			else:
				next_move = None
				
				if len(moves_performed) > 0 and moves_performed[-1] in possible_moves:
					possible_moves.remove(moves_performed[-1])
				
				if next_x != None and next_y != None:
					prio_dir_x, prio_dir_y = None, None
					pos_x, pos_y = get_pos_x(), get_pos_y()
					
					if next_x > pos_x:
						prio_dir_x = East
					elif next_x < pos_x:
						prio_dir_x = West
						
					if next_y > pos_y:
						prio_dir_y = North
					elif next_y < pos_y:
						prio_dir_y = South
						
					if prio_dir_x in possible_moves[idx]:
						next_move = prio_dir_x

					if prio_dir_y in possible_moves[idx]:
						next_move = prio_dir_y
				
				if next_move == None:
					next_move = possible_moves[idx].pop()
				else:
					possible_moves[idx].remove(next_move)
				
				moves_performed.append(next_move)
				move(next_move)
				
		next_x, next_y = measure()
				
	harvest()
	return True