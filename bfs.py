def solve_bfs_it(graph, graph_key, start, target_node):
	queue = [start]
	visited = set([start])
	parents = {}
			
	if start == target_node:
		return True
	
	while len(queue) > 0:
		current = queue.pop(0)
		
		if not (current in graph_key):
			continue
			
		if current == target_node:
			return reconstruct_path(parents, current, start)
		
		for neighbour in graph[current]:
			if not (neighbour in visited):
				queue.append(neighbour)
				visited.add(current)
				parents[neighbour] = current
	
	return False
