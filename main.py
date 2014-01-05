import sys
import os
from random import randint
from collections import OrderedDict
from graph import *
from tecla import Tecla

'''
Load primary and secondary representation
of keys into the keyboard object
'''
def load(dict):
	# QWERTY Keboard offsets
	offset = [1, 1.5, 1.3, 0, 0, 0]
	keyboard = []
		
	# read standard + shift layouts
	x, y = (1 + offset[0], 1)
	f = open(dict + '.txt')
	f_s = open(dict + '-shift.txt')
	lines = f.readlines()
	lines_s = f_s.readlines()
	# start from bottom row
	lines = lines[::-1]
	lines_s = lines_s[::-1]
	
	# keep the goddamn order!
	row = OrderedDict()
	# iterate both layouts simultaneously
	for line in zip(lines, lines_s):
		for key in line[0]:
			# row change, shift offset
			if key == '\n':
				keyboard.append(row)
				y += 1
				x = 1 + offset[y-1]
				row = OrderedDict()
			# column change, add to row
			else:
				key_s = line[1][line[0].index(key)]
				tec = Tecla(x, y, key, key_s)
				x += 1
				row[key] = tec
	f.close()
	f_s.close()
	return keyboard


def main():
	if len(sys.argv) != 4:
		print "[*] %s <tamano> <dictionary> <depth>" % sys.argv[0]
		return
	dict = sys.argv[2]
	# Load key distribution from file
	keyboard = load(dict)
	adj_matrix = fill_adjacent(keyboard)
	while True:
		c = raw_input('-------- Seleccione una letra: ')
		d = raw_input('Es adyacente con _______ ?')
		print '\n[*] NODO [*]'
		print 'Adj: ' + str(is_adjacent(adj_matrix, c, d))
		path = find_path(adj_matrix, c, d, int(sys.argv[3]))
		print 'Found path: %s' % path
		paths = find_paths(adj_matrix, c, d)
		print paths
		key = get_key(keyboard, c)
		rsp = key.get_char()
		#for i in range(int(sys.argv[1])):
		adj = get_adjacent(keyboard, key)
		print adj
		#	next = adj[randint(0, len(adj)-1)]
		#	rsp += next
		#	key = get_key(keyboard, next)
	#print_center(layout, key)

main()