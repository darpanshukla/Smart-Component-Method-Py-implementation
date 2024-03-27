import __init__ as im
import math
import random
def syscheckTested():
	## SYSCHECK function For Tested System
	if im.state[1] != 1:
		return 0
	else:
		return 1

def syscheckDB4():
	sys = 0
	for i in range(len(im.II)):
		sys = sys + checkreachability(im.II[i])
	if sys >= 2:
		return 1
	else:
		return 0


def syscheckDB4_10():
	
	e2  = fun2by3([ im.state[4-1], im.state[5-1], im.state[6-1] ])
	e3  = fun2by3([ im.state[1-1], im.state[2-1], im.state[3-1] ])
	
	e17 = funand([ im.state[1-1], im.state[2-1], im.state[3-1] ])
	e18 = funand([ im.state[4-1], im.state[5-1], im.state[6-1] ])
	
	e16 = funor([  e17, e18 ])
	
	e15 = funor([  im.state[7-1], im.state[8-1], im.state[9-1] ])
		
	e12 = funand([ e15, e16 ])
	
	e14 = funor([  im.state[9-1], im.state[10-1] ])
	
	e11 = funand([ im.state[1-1], im.state[2-1], e14 ])
	
	e4  = funor([  e11, e12 ])
	
	e1  = funor([  e3, e4 ])
	
	sys = funor([  e1, e2 ])

	return sys
	
	
def funor(x):
	state = 1
	if (0 in x) or (2 in x):
		state = 0
	else:
		state = 1
	return state

def funand(x):
	state = 1
	if x.count(1) > 1:
		state = 1
	else:
		state = 0
	return state
	
def fun2by3(x):
	state = sum(x)
	if state < 2:
		state = 0
	else:
		state = 1
	return state	

def syscheck3():

	sys = [0 for i in range(len(im.II))]
	for i in range(len(im.II)):
		sys[i] += checkreachability(im.II[i])
	
	if ((sys[0] ) == 1 and (sys[3] + sys[4]) == 2) and (sys[1] == 1 and (sys[5] + sys[6]) == 2):
		return 1
	elif (sys[1]  == 1 and (sys[5] + sys[6]) == 2) and (sys[2] == 1 and (sys[7] + sys[8]) == 2):
		return 1
	elif (sys[0] == 1 and (sys[3] + sys[4]) == 2) and (sys[2] == 1 and (sys[7] + sys[8]) == 2):
		return 1
	else:
		return 0

def syscheck3_sds4():

	sys = [0 for i in range(len(im.II))]
	for i in range(len(im.II)):
		sys[i] += checkreachability(im.II[i])
	
	if ((sys[0] + sys[1] ) == 2 and (sys[6] + sys[7]) >= 1) and ( (sys[2]+ sys[3]) == 2  and (sys[8] + sys[9]) >= 1):
		return 1
	elif ((sys[2] + sys[3]) == 2 and (sys[8] + sys[9]) >= 1) and ((sys[4]+ sys[5]) == 2 and (sys[10] + sys[11]) >= 1):
		return 1
	elif ((sys[0] + sys[1] ) == 2 and (sys[6] + sys[7]) >= 1) and ((sys[2] + sys[3]) == 2 and (sys[8] + sys[9]) >= 1):
		return 1
	else:
		return 0
	
	## Case-1: One Component
	
	## Case-2: Two Dependent Tested System
	# if im.state[1] in [0, 2]:
		# return 0
	# else:
		# return 1
	
	## Case-2: Two component Series Tested System 
	# if im.state[1] != 1 or im.state[0] != 1:
		# return 0
	# else:
		# return 1
	
	## Case-2: Two component Parallel Tested System 
	# if im.state[1] != 1 and im.state[0] != 1:
		# return 0
	# else:
		# return 1
		
	## Case-2: Three Component Dependency Tested System 
	# if im.state[1] != 1:
		# return 0
	# else:
		# return 1
	
	# sys = sum(im.state)
	# if sys >= 2:
		# return 1
	# else:
		# return 0		


		
def checkreachability(II):
	e       = im.conn[list(im.conn.keys())[0]]
	B       = int(II[0])
	stack   = []
	while 1:
		for i2 in e:
			if int(i2[ 0 ]) == B:
				stack.append( i2 )
		OldB = B
		
		while len( stack )!= 0:
			temp = stack.pop()
			if int( im.state[temp[ 0 ]] ) == 1:# If Not Failed
				if int(temp[2]) == int(II[1]):
					B       = temp[2]
					# print 'rechable',
					return 1;
				else:
					B       = temp[2]
					break
		if len(stack)==0 and OldB==B:
			# print 'Not Reachable'
			return 0;