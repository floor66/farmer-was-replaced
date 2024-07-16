def solve_bfs(graph, current, target_node, visited=None, path=None):
	if visited == None:
		visited = set()
	
	if path == None:
		path = []
	
	visited.add(current)

	if target_node in graph[current]:
		return path + [target_node]
	
	for neighbour in graph[current]:
		if neighbour in graph and not (neighbour in visited):
			new_path = solve_bfs(graph, neighbour, target_node, visited, path + [neighbour])
			if new_path != False:
				return new_path
	
	return False

def solve_bfs_it(graph, start, target_node):
	queue = [start]
	visited = set([start])
	parents = {}
	
	if start == target_node:
		return reconstruct_path(parents, current, start)
	
	while len(queue) > 0:
		current = queue.pop(0)
		
		if not (current in graph):
			continue
			
		if current == target_node:
			return reconstruct_path(parents, current, start)
		
		for neighbour in graph[current]:
			if not (neighbour in visited):
				queue.append(neighbour)
				visited.add(current)
				parents[neighbour] = current
	
	return False
