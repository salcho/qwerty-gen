import sys
import os
from optparse import OptionParser
from random import randint
from collections import OrderedDict
from graph import Graph
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

def print_banner():
	print '\n'
	print '{:-^70}'.format('[*] qwerty-gen [*]')
	print '{:-^70}'.format("[*] Keyboard sequences' generator for password cracking [*]")
	print '{:-^70}'.format('[*] Written at .co by: salcho - salchoman@gmail.com [*]')
	print '\n'

def main():
	print_banner()
	parser = OptionParser(usage="Usage: %prog [options] ")
	parser.add_option("-l", "--len", dest="depth", type="int", help="Password length [default: 6]", default=6)
	parser.add_option("-d", "--dict", dest="dict", type="string", help="Path to keyboard layout file [default: es-latin]", default='es-latin')
	parser.add_option("-k", "--key", dest="key", type="string", help="Key execution mode. Won't generate list.", default=False)
	parser.add_option("-p", "--perms", dest="perm", action="store_true", help="Generate shift permutations as well", default=False)
	parser.add_option("-v", "--verb", dest="verbose", action="store_true", help="General stats")
	parser.add_option("-o", "--out", dest="out", type="string", help="Path to output file [default: out.txt]", default='out.txt')

	(options, args) = parser.parse_args()
	dict = options.dict
	depth = options.depth
	key = options.key
	verbose = options.verbose
	perm = options.perm
	out = options.out

	if len(sys.argv) <= 1:
		print '[*] All options are set to default'
		print '[*] Passwords will have length %d' % depth
		print '[*] Dictionary files correspond to %s' % dict
		print '[*] No permutations will be generated'
		print '[*] Output file is %s' % out
		print '[*] Output on shell will be verbose'
		raw_input('Press any key to continue with these settings...')
	
	# Load key distribution from file
	keyboard = load(dict)
	graph = Graph(keyboard)
	if verbose:
		graph.print_stats()
	if key:
		c = raw_input('-------- Seleccione una letra: ')
		d = raw_input('Es adyacente con _______ ?')
		print '\n[*] ---------NODO-------- [*]'
		key = graph.get_key(c)
		rsp = key.get_char()
		print '[*] Adjacent? ' + str(graph.is_adjacent(c, d))
		adj = graph.get_adjacent(key)
		print '[*] Adacency matrix: %s' % adj
		path = graph.find_path(c, d, depth)
		if path:
			print '[*] First path of length %d -> %s' % (depth, ''.join(path))
			print '[*] All permutations are: %s' % graph.find_perms(''.join(path))
			path = graph.min_path(c, d, depth)
			print '[*] Minimum length for path: %d' % len(path)
			print '[*] Minimum path: %s' % path
			path = graph.max_path(c, d, depth)
			print '[*] Maximum length for path: %d' % len(path)
			print '[*] Maximum path: %s' % path			
			paths = graph.find_paths(c, d, depth)
			print '[*] Found %d paths of length %d\n ' % (len(paths), depth)
			#out = open('out.txt', 'w')
			#for cnt, p in zip(range(len(paths)), paths):
			#	out.write('[%d] %s\n' % (cnt, p))
			#out.close()
		else:
			print '[-] No path found between %s and %s : Increase length!' % (c, d)
	else:
		raw_input('[*] Press any key to start...')
		graph.generate_upto(depth, perm, out)
	
main()