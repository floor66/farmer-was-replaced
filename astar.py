def solve_astar(graph, start, target_node):
	target_node_x, target_node_y = idx_to_coords(target_node)

	def h(node):
		node_x, node_y = idx_to_coords(node)
		dx = abs(target_node_x - node_x)
		dy = abs(target_node_y - node_y)
		return dx + dy

	came_from = {}

	g_score = {}
	f_score = {}
	for key in graph:
		g_score[key] = globals["infinity"]
		f_score[key] = globals["infinity"]
	
	g_score[start] = 0
	f_score[start] = h(start)

	open_set = min_heapify([start], f_score)
	while not open_set["is_empty"]():
		current = open_set["pop_min"]()
		
		if current == target_node:
			return reconstruct_path(came_from, current, start)
		
		for neighbor in graph[current]:
			if not (neighbor in graph):
				continue
			
			tentative_g_score = g_score[current] + 1
			if tentative_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				neighbor_x, neighbor_y = (neighbor // globals["world_size"], neighbor % globals["world_size"])
				f_score[neighbor] = tentative_g_score + (abs(target_node_x - neighbor_x) + abs(target_node_y - neighbor_y))
				if not open_set["in"](neighbor):
					open_set["insert"](neighbor)
		
	return False
