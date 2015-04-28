#!/usr/bin/env python
# -*- coding: utf8 -*- 

INDENT = 4
SPACE = " "
NEWLINE = "\n"

def to_json(o, level=0):
	"""
	Provided [here](http://stackoverflow.com/questions/10097477/python-json-array-newlines) 
	by [Jeff Terrace](http://jeffterrace.com/).
	Brunetto Ziosi added the sorted.
	"""
	ret = ""
	if isinstance(o, dict):
		ret += "{" + NEWLINE
		comma = ""
		for k,v in iter(sorted(o.iteritems())):
			ret += comma
			comma = ",\n"
			ret += SPACE * INDENT * (level+1)
			ret += '"' + str(k) + '":' + SPACE
			ret += to_json(v, level + 1)

		ret += NEWLINE + SPACE * INDENT * level + "}"
	elif isinstance(o, basestring):
		ret += '"' + o + '"'
	elif isinstance(o, list):
		ret += "[" + ",".join([to_json(e, level+1) for e in o]) + "]"
	elif isinstance(o, bool):
		ret += "true" if o else "false"
	elif isinstance(o, int):
		ret += str(o)
	elif isinstance(o, float):
		ret += '%.7g' % o
	elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.integer):
		ret += "[" + ','.join(map(str, o.flatten().tolist())) + "]"
	elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.inexact):
		ret += "[" + ','.join(map(lambda x: '%.7g' % x, o.flatten().tolist())) + "]"
	else:
		raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
	return ret
