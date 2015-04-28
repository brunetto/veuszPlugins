#!/usr/bin/env python
# -*- coding: utf8 -*- 

#import json # overridden by custom function
import numpy as np

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

#####################
### MAIN FUNCTION ###
#####################

if __name__== "__main__":

	# Are you creating the plot structure or just refreshing the data?
	buildPlot = True
	
	xData = np.arange(100) 
	yData = np.random.randint(0, 100, size=100) + np.sin(np.arange(100))		
	
	# The same for the json file and the vuesz doc
	dataNameX = "xData"
	dataNameY = "yData"
	
	dataOut = {}
	
	dataOut[dataNameX] = xData
	dataOut[dataNameY] = yData
	
	out_file = open("outfile.json","w")
	####json.dump(dataOut,out_file,indent=4,sort_keys=True)
	out_file.write(to_json(dataOut))
	out_file.flush()
	out_file.close()

	if buildPlot:
		
		import veusz.embed as ve
		
		document = ve.Embedded("doc_1")

		pageWidth = "10cm"
		#pageHeight = "10cm"

		page = document.Root.Add('page', width=pageWidth)#, height=pageHeight)
		
		# How to set page properties after the page creation
		page.height.val = "10cm"
		
		gridRows = 1
		gridColumns = 1

		grid = page.Add('grid', autoadd=False, columns = gridColumns, rows = gridRows, 
								bottomMargin='0cm',
								leftMargin='0cm',
								rightMargin='0cm',
								topMargin='0cm'
								)
	
		graph = grid.Add('graph', autoadd=False)

		xAxis = graph.Add('axis', name='x', label = "")
		yAxis = graph.Add('axis', name='y', label = "")
		xy = graph.Add('xy', marker = 'none')#, step = 'left')
		#xy.PlotLine.steps.val = "left" # if you are makeing an histogram and want to set this after the plot creation
		
		#dataNameX and dataNameY are the same used for the json file
		# Document linking thanks to Ale Trani
		document.ImportFilePlugin(u'LoadJSON', u'outfile.json', linked=True, name=u'name')

        #document.SetData(dataNameX, xData)
		#document.SetData(dataNameY, yData)
		xy.xData.val = dataNameX
		xy.yData.val = dataNameY
			
		document.Save("example.vsz")
		document.Export("example.pdf")
		
		
