#!/usr/bin/python
'''
calling the class and obtaining the data from the database
'''
import os
import __init__ as im
#print im.__doc__
import global_data as gdata
import time
from copy import deepcopy
#import pylab as pl

## ==============  Simulation Parameters  ==================

#############################################
##System simulator model definition 
im.Model     = 1
'''
model == 0,1,2,3 for Mission time model, 
		4,5 for Regenerative Process model, 
		6 complete solution for steady state availability using Markov Regenerative process
'''
#############################################


#############################################
## Simulation parameters
im.MBatch    = 2
im.N         = int(1e4)
im.MT        = 30

#Acceleration parameters
im.x         = [0.85,0.45]#for firsttime == 1 or 2
im.firsttime = 82
im.accL      = 1e-3#for firsttime == 81
#############################################
'''
## Meaning to the Value of 'acceleration' variable
## 1 for both failure biasing and Forced Transition
## 2 for only failure biasing
## 3 for only Forced Transition
## 31 for only Forced Transition in regenerative repairable tested system
## 4 for group based failure sampling
## 5 for Scaled Biasing Technique
## 6 for Balanced Failure Biasing
## 7 for Approximate TestRate Model
## 81 for Time Dependent Reliability and Unavailability Calculations (Mission) Marseguarra Article - " exponential biasing - Sec 4.1"
## 82 for Time Dependent Reliability and Unavailability Calculations (Mission) Marseguarra Article - " uniform distribution biasing - Sec 4.5"
'''
# print 'Acceleration=%d (parameter=%f)'%(im.firsttime,im.x[0])
# print 'Batch=',im.MBatch, im.N

if im.Model == 0:
	'''
	Model        = Mission time
	Calculations = Static 
	Options		 = steady state / mission time only
	'''
	from s_ss_mission_time import main
	main()
elif im.Model == 1:
	'''
	Model        = Mission time
	Calculations = Static
	Options		 = Transient  + Steady state
	'''
	from s_t_mission_time import main
	main()
elif im.Model == 2:
	'''
	Model        = Mission time
	Calculations = Dynamic
	Options		 = steady state / mission time only
	'''
	from d_ss_mission_time import main
	main()
elif im.Model == 3:
	'''
	Model        = Mission time
	Calculations = Dynamic
	Options		 = Transient  + Steady state
	'''
	from d_t_mission_time import main
	main()
elif im.Model == 4:
	'''
	Model        = Regenerative process
	Calculations = Static
	Options		 = steady state / mission time only
	'''

	from s_regenerative import main
	main()
elif im.Model == 5:
	'''
	Model        = Regenerative process
	Calculations = Static
	Options		 = steady state / mission time only
	'''
	from s_t_regenerative import main
	main()
elif im.Model == 6:
	
	from s_complete_solution import main
	main()
