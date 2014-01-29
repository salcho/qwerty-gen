qwerty-gen
==========

Wordlist generator for apparent complex passwords

=============================

Generates keyboard sequences for a given layout to be used in password cracking

Developed by: salcho - salchoman[at]gmail.com


Features
==========
* Loads a given keyboard layout to a python graph. This is generic for all kind of keyboards (ATMs, cell phones, qwerty,   dvorak, etc.)
* Look for valid paths between all keys using limited Depth-First Search. Generates all possible patterns.
* Calculate all permutations for a given pattern in which Shift is pressed at any time.
* Print output to a dictionary file where it can be used against hashes passwords or authentication systems.


Usage
==========

* Keyboard layout is read from two dictionary files, e.g. en-us.txt and en-us-shift.txt
* Will use all default values if no parameters are received
* Requires Python 2.7!

  -h, --help            show this help message and exit
  -l DEPTH, --len=DEPTH
                        Password length [default: 6]
  -d DICT, --dict=DICT  Path to keyboard layout file [default: es-latin]
  -k KEY, --key=KEY     Key execution mode. Will only print info about the
                        key.
  -p, --perms           Generate shift permutations as well
  -v, --verb            General stats
  -o OUT, --out=OUT     Path to output file [default: out.txt]
  
  
Examples
===========
  * Generate all patterns of adjacent keys with a length of 7. Show stats and print to out_enus file
        $ ./qwerty-gen -l 7 -d en-us -v -o out_enus

  * Generate all patterns of adjacent keys with a length of 6. Calculate shift-permutations
        $ ./qwerty-gen -p -d en-us -v -o out_perms_enus

  * Show adjacent keys, regular and shift values for key 'f'
        $ ./qwerty-gen -k f
