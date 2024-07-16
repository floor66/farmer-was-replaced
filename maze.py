G_world_size = get_world_size()

def reconstruct_path(parents, current, start):
	path = []
	while current != start:
		path.append(current)
		current = parents[current]
	return path[::-1]

def moveTo(dest_x, dest_y):
	moves = []
	
	diff_x = dest_x - get_pos_x()
	dir = East
	if diff_x < 0:
		dir = West
	for i in range(abs(diff_x)):
		moves.insert(i, dir)
	
	diff_y = dest_y - get_pos_y()
	dir = North
	if diff_y < 0:
		dir = South
	for i in range(abs(diff_y)):
		moves.insert(i, dir)
	
	for m in moves:
		move(m)

def get_adjectend_nodes(plot_index, exclude=[]):
	connected_nodes = []
	plot_x, plot_y = idx_to_coords(plot_index)
	moves = [North, East, South, West]
	opposite_moves = [South, West, North, East]
	coord_mutations = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	
	for i in range(len(moves)):
		connected_x = plot_x + coord_mutations[i][0]
		connected_y = plot_y + coord_mutations[i][1]
		connected_idx = coords_to_idx(connected_x, connected_y)
		
		if connected_idx in exclude:
			continue
		
		if move(moves[i]):
			connected_nodes.append(connected_idx)
			move(opposite_moves[i])
		
	return connected_nodes

# Use backtracking to find the treasure and build the graph as we go
def solve_backtrack(graph, graph_key, node, visited=[]):
	node_x, node_y = idx_to_coords(node)
	moveTo(node_x, node_y)
	visited.append(node)
	
	if node in graph_key:
		candidates = graph[node] + get_adjectend_nodes(node, graph[node])
	else:
		candidates = get_adjectend_nodes(node)
		graph[node] = candidates
		graph_key.add(node)
	
	if get_entity_type() == Entities.Treasure:
		return True
	
	for candidate in candidates:
		if candidate in visited:
			continue
		
		if solve_backtrack(graph, graph_key, candidate, visited):
			return True
		else:
			# Dead end reached
			# Step back to the parent node, explore another branch
			moveTo(node_x, node_y)
	
	return False

def maze(solvers, solvernames, maxdepth=50):
	master_graph_key = set()
	master_graph = {}
	next_treasure_idx = None
	
	for maze_iterations in range(maxdepth - 1):
		# First, we get a maze
		if get_entity_type() != Entities.Hedge:
			if get_entity_type() != Entities.Treasure:
				plant(Entities.Bush)
			
			while get_entity_type() != Entities.Hedge:
				if not trade(Items.Fertilizer):
					print("Need fertilizer for Maze!")
					return False
				use_item(Items.Fertilizer)
		
		curr_idx = coords_to_idx(get_pos_x(), get_pos_y())
		solved = False
		
		if next_treasure_idx != None:
			if next_treasure_idx in master_graph_key and curr_idx in master_graph_key:
				if solvers == None:
					solvernames = ["dfs (rec)", "dfs (it) ", "bfs (it) ", "a*       "]
					solvers = [solve_dfs, solve_dfs_it, solve_bfs_it, solve_astar]
				
				paths = []
				c = 0
				for solver in solvers:
					solver_start_time = get_time()
					paths.append((solvernames[c], solver(master_graph, master_graph_key, curr_idx, next_treasure_idx), get_time() - solver_start_time))
					c += 1
				
				for result in paths:
					solvername, path, time = result
					if path == False:
						pathlen = -1
					else:
						pathlen = len(path)
					
					quick_print(solvername,":", pathlen, "in", time)
				quick_print("")
				pass
					
#					if path != False:
#						for p in path:
#							p_x, p_y = idx_to_coords(p)
#							moveTo(p_x, p_y)
#							master_graph[p] = master_graph[p] + get_adjectend_nodes(p, master_graph[p])
#						solved = True
	
		if not solved:
			if solve_backtrack(master_graph, master_graph_key, curr_idx):
				next_treasure_x, next_treasure_y = measure()
				next_treasure_idx = coords_to_idx(next_treasure_x, next_treasure_y)
			else:
				print("Unreachable")
				return False
		else:
			next_treasure_x, next_treasure_y = measure()
			next_treasure_idx = coords_to_idx(next_treasure_x, next_treasure_y)
						
	return True

start_count = get_op_count()
start_time = get_time()
if maze(None, None, 25):
	print(get_op_count() - start_count, "ops in", get_time() - start_time, "sec")
	# harvest()
