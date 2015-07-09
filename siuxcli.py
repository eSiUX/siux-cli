#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# SiUX command line client
# 

import sys, pprint
sys.path.append( '../siux-python/src/' )

from siuxmethodlib import methodArgs
import siuxlib

print 
print "SiUX command line client"
print
print



# wrong argument
if len(sys.argv) < 2:

	print "Use: "
	print
	print " ./siuxcli.py help "
	print

	sys.exit(1)



# help manual
if sys.argv[1] == 'help':

	print "Help:"
	print
	print "./siuxcli.py --ARGS METHOD_NAME "
	print

	methodSort = methodArgs.keys()
	methodSort.sort()
	__parent = ''

	for methodName in methodSort:

		__params = []

		__paramSort = methodArgs[methodName]['params'].keys()
		__paramSort.sort()

		for p in __paramSort:

			__paramVal = methodArgs[methodName]['params'][p]
			if not __paramVal:
				__paramVal = '""'

			__params.append( '--%s=%s' % (p, __paramVal ) )


		if __parent != methodArgs[methodName]['parent']:
			print
			print "Methods for %s:" % methodArgs[methodName]['parent']
			print

		print "- %s:" % methodName 
		print "\t./siuxcli.py %s %s" % (' '.join(__params), methodName)
		print

		__parent = methodArgs[methodName]['parent']
		del __params, __paramSort
	
	print
	sys.exit(1)


# ---
# run method


# method
methodName = sys.argv[-1]

# method not found
if methodName not in methodArgs:
	print "Error:"
	print
	print 'Method "%s" not exist' % (methodName,)
	print
	print
	print 'Use:'
	print
	print './siuxcli.py help'
	print
	sys.exit(1)


# param for method
methodArg = methodArgs[ methodName ]
params = {}
for p in sys.argv[1:-1]:

	# param parse
	ps = p.split('=')
	if len(ps) != 2:
		continue

	# param name=val
	pName = ps[0][2:]
	pVal  = ps[1] 

	# param name
	if pName not in methodArg['params']:
		print "Error:"
		print 
		print 'Parametr "%s" for method "%s" not exist' % (pName, methodName)
		print 
		print 'Use:'
		print
		print './siuxcli.py help'
		print
		sys.exit(1)

	# param value
	if pVal:
		try:
			pVal = int(pVal)
		except:
			try:
				pVal = eval(pVal)
			except:
				pass

	
	params[ pName ] = pVal

# auth string
auth = params.get( 'client', '' )
if not auth:
	print "Error:"
	print
	print 'Parametr "client" must be input'
	print
	sys.exit(1)

# client init
siuxClient = siuxlib.SiUXclient( auth=auth )

# method call
methodTest = getattr( siuxClient, methodName )
ret = methodTest( **params )

print "Method: %s" % (methodName,)
print
print "Response:"
print "- status        :", ret['status']
print "- statusCode    :", ret['statusCode']
print "- statusMessage :", ret['statusMessage']

if 'found' in ret:
	print
	print "- found         :", ret['found']

if 'data' in ret:
	print
	print "- data          :"
	print
	pprint.pprint( ret['data'] )

print
print "done."

