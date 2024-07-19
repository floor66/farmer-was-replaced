# Classess implementation of the min-heap (used for A* pathing in the Maze)

# Create an empty min-heap or convert an existing array to a min-heap
def min_heapify(_arr=[]):
	_min_heap = {
		"arr": [],
		"size": 0
	}

	# Return the index of the parent of the node i
	def __parent(i):
		return (i - 1) // 2

	# Return the index of the left child of the node i
	def __left_child(i):
		return (i * 2) + 1

	# Return the index of the right child of the node i
	def __right_child(i):
		return (i * 2) + 2

	# Return the value of node i, or return the entire heap if i is unspecified or None
	def __get(i=None):
		if i == None:
			return _min_heap["arr"]
		elif i < 0:
			return None
		else:
			return _min_heap["arr"][i]
	
	# Return the current minimum value stored in the min-heap
	def __get_min():
		return _min_heap["arr"][0]
	
	# Swap values of two nodes around specified by index_a and index_b
	def __swap(index_a, index_b):
		temp = _min_heap["arr"][index_b]
		_min_heap["arr"][index_b] = _min_heap["get"](index_a)
		_min_heap["arr"][index_a] = temp
	
	# Insert a value into the min-heap, maintaining min-heap order
	def __insert(elem_value):
		_min_heap["arr"].append(elem_value)
		_min_heap["size"] += 1

		elem_index = _min_heap["size"] - 1
		while elem_index > 0:
			parent_index = _min_heap["parent"](elem_index)
			parent_value = _min_heap["get"](parent_index)

			if elem_value > parent_value:
				break

			# Swap the element with its parent
			_min_heap["swap"](elem_index, parent_index)
			elem_index = parent_index # Set the element's index to the parent's index

	# Pop off the lowest (root) value of the min heap, maintaining min-heap order
	def __pop_min():
		# Swap the first (root) and last values so we can pop() the root value off
		_min_heap["swap"](0, _min_heap["size"] - 1)
		
		min_value = _min_heap["arr"].pop()
		_min_heap["size"] -= 1

		# Now we need to heapify down from the new root
		_min_heap["min_heapify_down"](0)

		return min_value
	
	# Return whether the specified node i is a leaf (has no children)
	def __is_leaf(i):
		return _min_heap["left_child"](i) > _min_heap["size"] - 1 and _min_heap["right_child"](i) > _min_heap["size"] - 1
	
	# Re-order the min-heap from the specified node curr_index down
	def __min_heapify_down(curr_index):
		# Stop when 1) we hit a leaf or 2) the current value is smaller than both of its children
		while not _min_heap["is_leaf"](curr_index):
			left_child = _min_heap["left_child"](curr_index)
			right_child = _min_heap["right_child"](curr_index)

			if _min_heap["get"](curr_index) > _min_heap["get"](left_child):
				_min_heap["swap"](curr_index, left_child)
				curr_index = left_child
			elif _min_heap["get"](curr_index) > _min_heap["get"](right_child):
				_min_heap["swap"](curr_index, right_child)
				curr_index = right_child
			else:
				break
	
	# Hack because we can't use classes, so we use a dict
	_min_heap["parent"] = __parent
	_min_heap["left_child"] = __left_child
	_min_heap["right_child"] = __right_child
	_min_heap["get"] = __get
	_min_heap["get_min"] = __get_min
	_min_heap["swap"] = __swap
	_min_heap["insert"] = __insert
	_min_heap["pop_min"] = __pop_min
	_min_heap["is_leaf"] = __is_leaf
	_min_heap["min_heapify_down"] = __min_heapify_down

	# If an array was specified in creating the min-heap, min-heapify it
	if len(_arr) > 0:
		for V in _arr:
			_min_heap["insert"](V)

	return _min_heap

# Various tests to make sure our min-heap works according to plan
def test_min_heap():
	# Check whether the constraints of the min heap apply to all nodes
	def validate_min_heap(heap):
		valid = []
		for X in range(heap["size"]):
			valid.append(heap["is_leaf"](X) or
							heap["get"](X) < heap["get"](heap["left_child"](X)) or
								heap["get"](X) < heap["get"](heap["right_child"](X)))
		return sum(valid) == heap["size"]
	
	# Create an empty min-heap and append some values in a random order
	arr_heapified = min_heapify()
	arr_heapified["insert"](30)
	arr_heapified["insert"](50)
	arr_heapified["insert"](20)
	arr_heapified["insert"](10)
	arr_heapified["insert"](80)
	arr_heapified["insert"](60)
	arr_heapified["insert"](70)

	quick_print("1", validate_min_heap(arr_heapified))

	# Insert and pop off a new (lowest) value
	arr_heapified["insert"](5)
	quick_print("2", arr_heapified["pop_min"]() == 5)

	quick_print("3", validate_min_heap(arr_heapified))

	# Create a min heap, supplying an array to start with
	arr_heapified = min_heapify([10, 20, 30, 50, 60, 70, 80])
	quick_print("4", validate_min_heap(arr_heapified))

	# Intentionally supply an incorrect min-heap, this should _not_ validate
	arr_heapified = min_heapify([10, 20, 30, 50, 60, 70, 80])
	arr_heapified["arr"] = [80, 70, 60, 50, 30, 20, 10]

	quick_print("5", not validate_min_heap(arr_heapified))

# Compare the min-heap to a normal array where we search all values for the lowest
# Note that while retrieving the min value is obviously faster,
# inserting values is quite slow as the game has a fixed time per operation
# and it costs more operations due to the "class" structure
def benchmark():
	size = 10000
	
	seq = []
	for _ in range(size):
		rnd = random() * 1000 // 1
		seq.append(rnd)
	seq_heap = min_heapify(seq)

	st = get_time()
	lowest_val = seq_heap["pop_min"]()
	quick_print(lowest_val)
	quick_print("min-heap", get_time() - st)
	quick_print("")

	st = get_time()
	lowest_val = None
	for K in range(len(seq)):
		if lowest_val == None or seq[K] < lowest_val:
			lowest_val = seq[K]
	quick_print(lowest_val)
	quick_print("bruteforce", get_time() - st)
