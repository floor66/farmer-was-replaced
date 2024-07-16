def solve_astar(graph, graph_key, start, target_node):
	def h(node):
		node_x, node_y = idx_to_coords(node)
		target_node_x, target_node_y = idx_to_coords(target_node)
		dx = abs(target_node_x - node_x)
		dy = abs(target_node_y - node_y)
		return (dx * dx) + (dy * dy)

	openSet = set([start])
	cameFrom = {}
	
	gScore = {}
	fScore = {}
	for key in graph_key:
		gScore[key] = infinity()
		fScore[key] = infinity()
	
	gScore[start] = 0
	fScore[start] = h(start)
	while len(openSet) > 0:
		current = None
		
		# Find node in openSet with lowest fScore
		for v in openSet:
			v_score = h(v)
			if current == None:
				current = (v, v_score)
			else:
				_, score = current
				if v_score < score:
					current = (v, v_score)
		
		current, _ = current
		
		if current == target_node:
			return reconstruct_path(cameFrom, current, start)
		
		openSet.remove(current)
		for neighbor in graph[current]:
			if not (neighbor in graph_key):
				continue
			
			tentative_gScore = gScore[current] + 1
			if tentative_gScore < gScore[neighbor]:
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore
				fScore[neighbor] = tentative_gScore + h(neighbor)
				if not neighbor in openSet:
					openSet.add(neighbor)
		
	return False
