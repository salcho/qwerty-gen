import math
import string
import time
from tecla import Tecla

class Graph:
	# Keyboard graph rulez
	def __init__(self, layout, charset=''):
		self.layout = layout
		self.adj_matrix = self.fill_adjacent()
		self.all_paths = []
		self._chardict = {'lower_alpha': string.ascii_lowercase, 'upper_alpha': string.ascii_lowercase, 'mixed_alpha': string.ascii_letters,
						  'digits': string.digits, 'special_char': string.punctuation}
		self.charset = self._chardict['mixed_alpha'] + self._chardict['digits']

	# Calculate basic stats
	def print_stats(self):
		cnt = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
		for k, v in self.adj_matrix.items():
			cnt[len(v)] += 1
			
		print "[*] Loaded graph with %d vertices (V) and %d edges (E)" % (len(self.adj_matrix), len(cnt.items()))
		print "[*] Vertices vs Edges: "
		print cnt.items()		

	'''
	Return key object given it's primary representation
	'''
	def get_key(self, c):
		for row in self.layout:
			for char, col in row.items():
				if char == c:
					#print col.to_str()
					return col
		return None

	'''
	This will find adjacent keys for a given key
	according to the neighborhood definition:
	l <= sqrt(2)
	[actually equal to rather than lower or equal]
	'''
	def get_adjacent(self, key):
		rsp = []
		for row in self.layout:
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
	def fill_adjacent(self):
		rsp = {}
		for row in self.layout:
			for char, key in row.items():
				rsp[char] = self.get_adjacent(key)
		return rsp

	def is_adjacent(self, a, b):
		return b in self.adj_matrix[a]

	'''
	Return first path between keys,
	no repetition, return first search
	mod: depht-fixed at max path length
	'''
	def find_path(self, a, b, max, path=[]):
		if max > 0:
			path = path + [a]
			if a == b:
				return path
			if a not in self.adj_matrix.keys():
				return None
			for node in self.adj_matrix[a]:
				if node not in path:
					if max == 1:
						continue
					new = self.find_path(node, b, max-1, path)
					if new:
						return new

	'''
	Return all paths of length len between keys
	Fixes output 
	'''
	def find_paths(self, a, b, leng):
		paths = self.find_all_paths(a, b, leng)
		# paths is a list in which each item corresponds to
		# all paths found for each neighboor of a, each path
		# separated by the : char
		cnt = 0
		all_paths = []
		for path in paths:
					all_paths.append(path)
		self.all_paths = all_paths
		return all_paths

	'''
	Return shortest path
	'''
	def min_path(self, a, b, leng):
		paths = self.find_paths(a, b, leng)
		shortest = None
		for p in paths:
			if not shortest or len(p) < len(shortest):
				shortest = p
		return shortest

	'''
	Return max length path
	'''
	def max_path(self, a, b, leng):
		paths = self.find_paths(a, b, leng)
		max = None
		for p in paths:
			if not max or len(p) > len(max):
				max = p
		return max

	'''
	Return all paths of length max between keys
	'''
	def find_all_paths(self, a, b, max, path=''):
		if max > 0:
			path = path + a
			if a == b:
				return path
			if a not in self.adj_matrix.keys():
				return None
			paths = []
			for node in self.adj_matrix[a]:
				if node not in path:
					new = self.find_all_paths(node, b, max-1, path)
					if new:
						if isinstance(new, basestring): new = [new]
						paths = paths + new
			return filter(None, paths)
		else:
			return None

	'''
	Return a hash table with all routes from node a to b in
	less than max hops. Generate shift permutations if perm
	flag. Output results to specified path.
	'''
	def generate_upto(self, max, perm, out):
		start_time = time.time()
		out = open(out, 'w')
		keys = self.adj_matrix.keys()
		total = 0
		count = 0
		size = 1
		while size <= max:
			try:
				for cnt, start in zip(range(len(keys)), keys):
					i = cnt + 1
					while i < len(keys):
						path = self.find_paths(start, keys[i], size)
						# Here we add an additional, inverse copy of the generated
						# password as we iterate through keypairs only once
						if path:
							for p in path:
								out.write(p + '\n')
								out.write(p[::-1] + '\n')
								# Generate shift permutations
								if perm:
									perms = self.find_perms(p)
									for perm in perms:
										out.write(perm + '\n')
										out.write(perm[::-1] + '\n')
										total += 2
								total += 2
						i += 1
				print '[*] Generated all passwords of length %d' % size
				print '[*] %d passwords have been generated' % total
				print '[*] ETA: {}'.format(self.hms_string(time.time() - start_time))
				count += total
				total = 0
				size += 1
				
			except KeyboardInterrupt:
				exit = raw_input('[-] Are you sure you want to exit? [y/n] ')
				if 'y' in exit:
					out.close()
					return
				else:
					print '[*] Generated all passwords of length %d' % size
					print '[*] %d passwords have been generated' % total
					print '[*] ETA: {}'.format(self.hms_string(time.time() - start))
					continue
			
		out.close()
		print '[*] Generated a total of %d passwords between 1 and %d characters.' % (count, max)
		return

	'''
	Find all possible permutations over a given string
	when each character can have two posible characters
	'''
	def find_perms(self, str):
		# We use a binary number to go through all possible
		# permutations of the given string of length n
		rsp = []
		control = 1
		while control < math.pow(2, len(str)):
			binn = bin(control)
			# skip characters 0b at the start of the number
			binn = binn[2:]
			# reverse number
			binn = binn[::-1]
			# pad with 0s
			binn += '0'*(len(str)-len(binn))
			
			# change original str according to bin
			tmp = list(str)
			for i, b in zip(range(len(binn)), binn):
				# if this bit is on then we swap chars at pos i
				if int(b):
					t = self.get_key(tmp[i])
					tmp[i] = t.get_shift()
			rsp += [''.join(tmp)]
			control += 1
		return rsp

	# Got this from http://arcpy.wordpress.com/2012/04/20/146/
	def hms_string(self, sec_elapsed):
		h = int(sec_elapsed / (60 * 60))
		m = int((sec_elapsed % (60 * 60)) / 60)
		s = sec_elapsed % 60.
		return "{}:{:>02}:{:>05.2f}".format(h, m, s)
	# End hms_string

	def get_charset(self):
		return self.charset
	def set_charset(self, charset):
		if charset in self._chardict.keys(): self.charset = charset
