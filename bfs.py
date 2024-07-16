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
	# Hacky workaround 'cause we cant use classes, so we just use a queue dict!
	queue = {
		"enqueue_stack": [],
		"dequeue_stack": []
	}

	def enqueue(item):
		queue["enqueue_stack"].append(item)
	
	def dequeue():
		if not queue["dequeue_stack"]:
			while queue["enqueue_stack"]:
				queue["dequeue_stack"].append(queue["enqueue_stack"].pop())
		
		if not queue["dequeue_stack"]:
			print("dequeue from empty queue")
			return foo()
		
		return queue["dequeue_stack"].pop()
	
	def is_empty():
		return not queue["enqueue_stack"] and not queue["dequeue_stack"]
	
	def size():
		return len(queue["enqueue_stack"]) + len(queue["dequeue_stack"])

	enqueue(start)
	visited = set([start])
	parents = {}
	
	if start == target_node:
		return reconstruct_path(parents, current, start)
	
	while not is_empty():
		current = dequeue()
		
		if not (current in graph):
			continue
			
		if current == target_node:
			return reconstruct_path(parents, current, start)
		
		for neighbour in graph[current]:
			if not (neighbour in visited):
				enqueue(neighbour)
				visited.add(current)
				parents[neighbour] = current
	
	return False
