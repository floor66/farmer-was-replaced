def reconstruct_path(parents, current, start):
	path = []
	while current != start:
		path.append(current)
		current = parents[current]
	return path[::-1]

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
def solve_backtrack(graph, node, visited=[]):
	move_to_idx(node)
	visited.append(node)
	
	if node in graph:
		candidates = graph[node] + get_adjectend_nodes(node, graph[node])
	else:
		candidates = get_adjectend_nodes(node)
		graph[node] = candidates
	
	if get_entity_type() == Entities.Treasure:
		return True
	
	for candidate in candidates:
		if candidate in visited:
			continue
		
		if solve_backtrack(graph, candidate, visited):
			return True
		else:
			# Dead end reached
			# Step back to the parent node, explore another branch
			move_to_idx(node)
	
	return False

def maze(maxdepth, solvers=None, solvernames=None):
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
			if next_treasure_idx in master_graph and curr_idx in master_graph:
				if solvers == None:
					solvernames = ["dfs (rec)", "dfs (it) ", "bfs (rec)", "bfs (it) ", "a*       "]
					solvers = [solve_dfs, solve_dfs_it, solve_bfs, solve_bfs_it, solve_astar]
				
				paths = []
				c = 0
				for solver in solvers:
					solver_start_time = get_time()
					paths.append((solvernames[c], solver(master_graph, curr_idx, next_treasure_idx), get_time() - solver_start_time))
					c += 1
				
				shortest_path, shortest_path_len = None, None
				for result in paths:
					solvername, path, time = result
					if path == False:
						pathlen = None
					else:
						pathlen = len(path)
						if shortest_path == None or pathlen < shortest_path_len:
							shortest_path = path
							shortest_path_len = pathlen
					
					quick_print(solvername,":", pathlen, "in", time)
				quick_print("")
					
				if shortest_path != None:
					for p in path:
						move_to_idx(p)
						master_graph[p] = master_graph[p] + get_adjectend_nodes(p, master_graph[p])
					solved = True
	
		if not solved:
			if solve_backtrack(master_graph, curr_idx):
				next_treasure_x, next_treasure_y = measure()
				next_treasure_idx = coords_to_idx(next_treasure_x, next_treasure_y)
			else:
				print("Unreachable")
				return False
		else:
			next_treasure_x, next_treasure_y = measure()
			next_treasure_idx = coords_to_idx(next_treasure_x, next_treasure_y)
						
	return True
