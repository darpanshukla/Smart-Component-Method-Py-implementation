#!/usr/bin/python
'''
calling the class and obtaining the data from the database
'''
import os
from dict_manipulation import mainfunction
from dict_manipulation import mainfunction1
import __init__ as im

# print '''
# Enter data base number
# 0 : 'DB4' 
# 1 : 'TestedSystemDB'
# 2 : 'DB1' - DHR system
# 3 : 'Shutdown System'
# 4 : Other systems
# '''
# im.DSNnumber = int(input('Enter the number from above'))

# if im.DSNnumber == 0:
	# from sys_simulation import *
	# im.DSNstr = 'DB4'
# elif im.DSNnumber == 1:
	# from sys_simulation import *
	# im.DSNstr = 'TestedSystemDB'
# elif im.DSNnumber == 2:
	# from sys_simulation_DB1_DHR import *
	# im.DSNstr = 'DB1'
# elif im.DSNnumber == 3:
	# from sys_simulation_SDS import *
	# im.DSNstr = 'ShutdownSysRod1'
if im.DSNstr not in ["DB4", "ShutdownSysRod1_1", "DB5"]:
	print( "Reading 'text' file for the input system description")
	[comps, compsdata, conn] = mainfunction(im.DSNstr)
else:
	print( "Reading 'Database' file for the input system description")
	[comps, compsdata, conn] = mainfunction1(im.DSNstr)
