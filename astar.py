def solve_astar(graph, start, target_node):
	target_node_x, target_node_y = idx_to_coords(target_node)

	def h(node):
		node_x, node_y = idx_to_coords(node)
		dx = abs(target_node_x - node_x)
		dy = abs(target_node_y - node_y)
		return dx + dy

	cameFrom = {}

	gScore = {}
	fScore = {}
	for key in graph:
		gScore[key] = infinity()
		fScore[key] = infinity()
	
	gScore[start] = 0
	fScore[start] = h(start)

	openSet = min_heapify([start], fScore)
	while not openSet["is_empty"]():
		current = openSet["pop_min"]()
		
		if current == target_node:
			return reconstruct_path(cameFrom, current, start)
		
		for neighbor in graph[current]:
			if not (neighbor in graph):
				continue
			
			tentative_gScore = gScore[current] + 1
			if tentative_gScore < gScore[neighbor]:
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore
				neighbor_x, neighbor_y = (neighbor // globals["world_size"], neighbor % globals["world_size"])
				fScore[neighbor] = tentative_gScore + (abs(target_node_x - neighbor_x) + abs(target_node_y - neighbor_y))
				if not openSet["in"](neighbor):
					openSet["insert"](neighbor)
		
	return False
