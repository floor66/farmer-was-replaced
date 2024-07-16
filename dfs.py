def solve_dfs(graph, graph_key, current, target_node, visited=None, path=None):
	if visited == None:
		visited = set()
	
	if path == None:
		path = []
	
	if current == target_node:
		return path
		
	visited.add(current)
	
	for child in graph[current]:
		if not (child in graph_key):
			continue

		if not (child in visited):
			child_path = solve_dfs(graph, graph_key, child, target_node, visited, path + [child])
			if child_path != False:
				return child_path
	
	return False

def solve_dfs_it(graph, graph_key, start, target_node):
	stack = [start]
	visited = set([start])
	parents = {}
	
	while len(stack) > 0:
		current = stack.pop()
		
		if current == target_node:
			return reconstruct_path(parents, current, start)

		if not (current in graph_key):
			continue
				
		for child in graph[current]:
			if not (child in visited):
				stack.append(child)
				visited.add(child)
				parents[child] = current
	
	return False
