#!/usr/bin/python
'''
********************************************************************************
********************************************************************************
********************************************************************************
********************************************************************************
********************************************************************************
********************************************************************************
********************************************************************************
********************************************************************************
WELCOME TO 
*          8888888          88888   888                  888  
*		 88888            88888		8888                8888
*	   88888            88888       88888              88888
*		88888         88888         888888            888888
*		  88888      88888          8888888          8888888
*		   888888    88888          88888888        88888888
*			888888    88888         8888 8888      8888 8888
*		   888888       88888       88888 8888    8888 88888
*		 888888           88888     88888  8888  8888  88888    
*	   88888                88888   88888   888888888  88888

--------------------------------------------------------------------------------
SMART COMPONENT FRAMEWORK FOR DYNAMIC RELIABILITY ANALYSIS OF DIGITAL I&C SYSTEM
--------------------------------------------------------------------------------

--
Developer : Darpan Krishnakumar Shukla
Guide     : Dr. A. John Arul
--
Starting Date of the Development : June 19, 2017
--
'''

from databaseio import *

from sample_simulation import *
from reliability_tally import *
# __all__ = ['dict_manipulation','databaseio','global_data']#

#The __init__.py files are required to make Python treat the directories as containing packages

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("OPFolder", type=str, help='''Output Folder Name''')
parser.add_argument("inputfile", type=str, help="Input File name")
args =  parser.parse_args()
# OPFolder = "op-p-1"
# inputfile = "ShutdownSysRod1_DIAGNOSTIC"
im.foldername= args.OPFolder
im.DSNstr = args.inputfile
from global_data import *

xtest= ["TestedSystemDB"] + ["TestedSystemDB_%d"%i for i in range(1,11)]
## Global rule 
## 1) for failure criteria
## 2) System state check
if im.DSNstr in xtest:
	from sys_simulation import syscheckTested as syscheck
elif im.DSNstr in ["ShutdownSysRod1", "ShutdownSysRod1_DIAGNOSTIC"] :
	from sys_simulation_SDS import syscheck_SDS2_RPS as syscheck
elif im.DSNstr == "ShutdownSysRod1Channel1" :
	from sys_simulation_SDS import syscheck_SDS2_RPS_Ch1 as syscheck
elif im.DSNstr in ["SDS1","SDS3","SDS1H","SDS3H","SDS3_Reduced"]:
	from sys_simulation_SDS import syscheck1 as syscheck
elif im.DSNstr in ["SDS2", "SDS5","SDS2H", "SDS5H"]:
	from sys_simulation_SDS import syscheck2 as syscheck
elif im.DSNstr in ["SDS4","SDS4H"]:
	from sys_simulation_SDS import syscheck3 as syscheck
elif im.DSNstr in ["SDS6","SDS6H"]:
	from sys_simulation_SDS import syscheck4 as syscheck
elif im.DSNstr in ["SDS7","SDS7H","SDS7H_independent"]:
	from sys_simulation_SDS import syscheck5 as syscheck
elif im.DSNstr == "DB1":
	from sys_simulation_SDS import syscheck1DHR as syscheck
elif im.DSNstr == "DB4" or im.DSNstr == "DB5":
	from sys_simulation import syscheckDB4 as syscheck
	
def initialization():
	im.te        = [ 0.0 for i in range( im.lenc ) ]#elapsed time of each comp
	im.state     = [ 1 for i in range( im.lenc) ]
	im.exec_seq  = deepcopy( im.perm_exec_seq )
	im.compsdata = deepcopy( im.permanent_initial_value )
	im.rates     = deepcopy( im.perm_init_rate )
	im.cutset    = []
	return
