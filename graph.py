import math

'''
Return key object given it's primary representation
'''
def get_key(layout, c):
	for row in layout:
		for char, col in row.items():
			if char == c:
				print col.to_str()
				return col
	return None

'''
This will find adjacent keys for a given key
according to the neighborhood definition:
l <= sqrt(2)
[actually equal to rather than lower or equal]
'''
def get_adjacent(layout, key):
	rsp = []
	for row in layout:
		for k,v in row.items():
			if v.get_coords() == key.get_coords():
				continue
			x, y = v.get_coords()
			l = math.pow(key.y() - y, 2) + math.pow(key.x() - x, 2)
			l = math.sqrt(l)
			if l <= math.sqrt(2):
				rsp.append(k)
	return rsp

'''
Create and return adjacency matrix for all keys
{'q':['w', 'a' ...]}
'''
def fill_adjacent(layout):
	rsp = {}
	for row in layout:
		for char, key in row.items():
			rsp[char] = get_adjacent(layout, key)
	return rsp

def is_adjacent(layout, a, b):
	return b in layout[a]

'''
Return first path between keys
mod: depht-fixed at max path length
'''
def find_path(layout, a, b, max, path=[]):
	if max > 0:
		path = path + [a]
		if a == b:
			return path
		if a not in layout.keys():
			return None
		for node in layout[a]:
			if node not in path:
				if max == 1:
					continue
				new = find_path(layout, node, b, max-1, path)
				if new:
					print new
					return new

'''
Return all paths between keys
'''
def find_paths(layout, a, b, path=[]):
	path = path + [a]
	if a == b:
		return path
	if a not in layout.keys():
		return None
		paths = []
		for node in layout[a]:
			if node not in path:
				new = find_paths(layout, node, b, path)
				for p in new:
					print p
					paths.append(p)
		return paths