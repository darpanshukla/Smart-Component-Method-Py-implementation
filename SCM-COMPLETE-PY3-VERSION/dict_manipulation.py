#!/usr/bin/python
'''
Program for dictionary manipulation and creating a dictionary object out of an input database file.
'''

def mainfunction(DSNstr):
    import pypyodbc
    import __init__ as im
    '''
    Reads input database table for components and connectors
    Input:
    DSN name e.g. 'TestedSystemDB'

    Returns:
    [Component table list, dict of all component tables data, connectin lists]

    '''

    ## Obtaining list of components, existing in a database for describing the system of interest

    outfile= open("%s.txt"%(DSNstr),'r')
    line = outfile.readlines()
    outfile.close()
    temp: list = eval(line[0])
    print(temp)
    # if DSNstr in ["SDS4"]:
        # im.II = [[i,40]for i in range(12)]
    # if DSNstr in ["ShutdownSysRod1"]:
        # im.II = [[i,31]for i in range(9)]
    im.permanent_initial_value = temp[1]
    im.exec_seq = temp[0]
    if DSNstr in ['1-Lewis-System-Revealed','1-Lewis-System-Unrevealed']:
        im.II = [[0,1]]
    elif DSNstr in ['2-Lewis-System']:
        im.II = [[0,2],[1,2]]
    elif DSNstr in ['2-Marseguerra-System']:
        im.II = [[0,2]]
    elif DSNstr in ['3-Marseguerra-System']:
        im.II = [[0,3],[1,3],[2,3]]
    else:
        pass
    return temp
def mainfunction2(DSNstr):

	'''
	Reads input database table for components and connectors
	Input:
	DSN name e.g. 'TestedSystemDB'
	
	Returns:
	[Component table list, dict of all component tables data, connectin lists]
	
	'''

	## Obtaining list of components, existing in a database for describing the system of interest

	outfile= open("%s.txt"%(DSNstr),'r')
	line = outfile.readlines()
	outfile.close()
	temp: list = eval(line[0])
	# if DSNstr in ["SDS4"]:
		# im.II = [[i,40]for i in range(12)]
	# if DSNstr in ["ShutdownSysRod1"]:
		# im.II = [[i,31]for i in range(9)]
	permanent_initial_value = temp[1]
	exec_seq = temp[0]
	II = [[0,1]]
	return temp
def mainfunction1(DSNstr):
	import pypyodbc
	import __init__ as im
	'''
	Reads input database table for components and connectors
	Input:
	DSN name e.g. 'TestedSystemDB'
	
	Returns:
	[Component table list, dict of all component tables data, connectin lists]
	
	'''

	#############################################
	## Connecting to the Database
	conn  = pypyodbc.connect( DSN = DSNstr )
	cur   = conn.cursor()
	
	#############################################
	## Obtaining list of components, existing in a database for describing the system of interest
	# # comp_table_list = []
	# # connector_table_list = []
	# # for row in cur.tables():
		# # #Since row is having list of both tables i.e. "SYSTEM(OS) TABLE" and "TABLE", IF statements is used in next line
		# # if row[3]=='TABLE':
			# # if raw_input('Is %s a component'%row[2])=='y':
				# # comp_table_list.append(row[2])
			# # elif raw_input('Is %s a connector'%row[2])=='y':
				# # connector_table_list.append(row[2])
	##########
	if DSNstr == 'ShutdownSysRod1' or DSNstr == 'ShutdownSysRod1_Copy':

		## SDS1-RPS1-PbyQ-1XA
		#comp_table_list =['NS_1XM','NS_1XN','ASP_NS_1XM','ASP_NS_1XN','OR_NS_1X','PbyQ_Compute_1XA','Manual_Test','PS']
		#connector_table_list = ['Connector_NS_PQ1X_RPS_SDS1']
		
		##SDS1-RPS1-PbyQ-1XA,B
		# comp_table_list =['NS_1XM','NS_1XN','ASP_NS_1XM','ASP_NS_1XN','OR_NS_1X','EM_FM_1XA','ASP_EMFM_1XA','EM_FM_1XB','ASP_EMFM_1XB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PQ_Comparator_1XA','PQ_Comparator_1XB','SLFIT_RPS_1','Manual_Test','PS']
		# connector_table_list = ['Connector_PQ1X_RPS_SDS1']
		
		##SDS1
		# comp_table_list= ['NS_1XM','NS_1XN','NS_1YM','NS_1YN','NS_1ZM','NS_1ZN','EM_FM_1XA','EM_FM_1XB','EM_FM_1YA','EM_FM_1YB','EM_FM_1ZA','EM_FM_1ZB','ASP_NS_1XM','ASP_NS_1XN','ASP_NS_1YM','ASP_NS_1YN','ASP_NS_1ZM','ASP_NS_1ZN','OR_NS_1X','OR_NS_1Y','OR_NS_1Z','ASP_EMFM_1XA','ASP_EMFM_1XB','ASP_EMFM_1YA','ASP_EMFM_1YB','ASP_EMFM_1ZA','ASP_EMFM_1ZB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PbyQ_Compute_1YA','PbyQ_Compute_1YB','PbyQ_Compute_1ZA','PbyQ_Compute_1ZB','PQ_Comparator_1XA','PQ_Comparator_1XB','PQ_Comparator_1YA','PQ_Comparator_1YB','PQ_Comparator_1ZA','PQ_Comparator_1ZB','SLFIT_RPS_1','Manual_Test','PS']
		# connector_table_list = ['Connector_RPS_SDS1']

		##SDS1-AS
		# comp_table_list=['SLFIT_RPS_1','Manual_Test','PS','SCRAM_SW_SDS1_1A','SCRAM_SW_SDS1_1B','CSR_1','SCRAM_SW_SDS1_2A','SCRAM_SW_SDS1_2B','CSR_2','SCRAM_SW_SDS1_3A','SCRAM_SW_SDS1_3B','CSR_3','SCRAM_SW_SDS1_4A','SCRAM_SW_SDS1_4B','CSR_4','SCRAM_SW_SDS1_5A','SCRAM_SW_SDS1_5B','CSR_5','SCRAM_SW_SDS1_6A','SCRAM_SW_SDS1_6B','CSR_6','SCRAM_SW_SDS1_7A','SCRAM_SW_SDS1_7B','CSR_7','SCRAM_SW_SDS1_8A','SCRAM_SW_SDS1_8B','CSR_8','SCRAM_SW_SDS1_9A','SCRAM_SW_SDS1_9B','CSR_9']
		# connector_table_list = ['Connector_AS_SDS1']
		
		##SDS1
		# comp_table_list= ['NS_1XM','NS_1XN','NS_1YM','NS_1YN','NS_1ZM','NS_1ZN','EM_FM_1XA','EM_FM_1XB','EM_FM_1YA','EM_FM_1YB','EM_FM_1ZA','EM_FM_1ZB','ASP_NS_1XM','ASP_NS_1XN','ASP_NS_1YM','ASP_NS_1YN','ASP_NS_1ZM','ASP_NS_1ZN','OR_NS_1X','OR_NS_1Y','OR_NS_1Z','ASP_EMFM_1XA','ASP_EMFM_1XB','ASP_EMFM_1YA','ASP_EMFM_1YB','ASP_EMFM_1ZA','ASP_EMFM_1ZB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PbyQ_Compute_1YA','PbyQ_Compute_1YB','PbyQ_Compute_1ZA','PbyQ_Compute_1ZB','PQ_Comparator_1XA','PQ_Comparator_1XB','PQ_Comparator_1YA','PQ_Comparator_1YB','PQ_Comparator_1ZA','PQ_Comparator_1ZB','SLFIT_RPS_1','SCRAM_SW_SDS1_1A','SCRAM_SW_SDS1_1B','CSR_1','SCRAM_SW_SDS1_2A','SCRAM_SW_SDS1_2B','CSR_2','SCRAM_SW_SDS1_3A','SCRAM_SW_SDS1_3B','CSR_3','SCRAM_SW_SDS1_4A','SCRAM_SW_SDS1_4B','CSR_4','SCRAM_SW_SDS1_5A','SCRAM_SW_SDS1_5B','CSR_5','SCRAM_SW_SDS1_6A','SCRAM_SW_SDS1_6B','CSR_6','SCRAM_SW_SDS1_7A','SCRAM_SW_SDS1_7B','CSR_7','SCRAM_SW_SDS1_8A','SCRAM_SW_SDS1_8B','CSR_8','SCRAM_SW_SDS1_9A','SCRAM_SW_SDS1_9B','CSR_9','Manual_Test','PS']
		# connector_table_list = ['Connector_SDS1']
		# failgp = [['NS_1XM','NS_1XN','NS_1YM','NS_1YN','NS_1ZM','NS_1ZN','EM_FM_1XA','EM_FM_1XB','EM_FM_1YA','EM_FM_1YB','EM_FM_1ZA','EM_FM_1ZB','ASP_NS_1XM','ASP_NS_1XN','ASP_NS_1YM','ASP_NS_1YN','ASP_NS_1ZM','ASP_NS_1ZN','OR_NS_1X','OR_NS_1Y','OR_NS_1Z','ASP_EMFM_1XA','ASP_EMFM_1XB','ASP_EMFM_1YA','ASP_EMFM_1YB','ASP_EMFM_1ZA','ASP_EMFM_1ZB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PbyQ_Compute_1YA','PbyQ_Compute_1YB','PbyQ_Compute_1ZA','PbyQ_Compute_1ZB','SLFIT_RPS_1','CSR_1','CSR_2','CSR_3','CSR_4','CSR_5','CSR_6','CSR_7','CSR_8','CSR_9'],['PQ_Comparator_1XA','PQ_Comparator_1XB','PQ_Comparator_1YA','PQ_Comparator_1YB','PQ_Comparator_1ZA','PQ_Comparator_1ZB','SCRAM_SW_SDS1_1A','SCRAM_SW_SDS1_1B','SCRAM_SW_SDS1_2A','SCRAM_SW_SDS1_2B','SCRAM_SW_SDS1_3A','SCRAM_SW_SDS1_3B','SCRAM_SW_SDS1_4A','SCRAM_SW_SDS1_4B','SCRAM_SW_SDS1_5A','SCRAM_SW_SDS1_5B','SCRAM_SW_SDS1_6A','SCRAM_SW_SDS1_6B','SCRAM_SW_SDS1_7A','SCRAM_SW_SDS1_7B','SCRAM_SW_SDS1_8A','SCRAM_SW_SDS1_8B','SCRAM_SW_SDS1_9A','SCRAM_SW_SDS1_9B','Manual_Test','PS']]
		
		
		##SDS2-RPS2-Line1
		# comp_table_list=['Manual_Test','PS','Thermo_CSAM1','ASP_TC_CSAM1','Comparator_TC_CSAM1']
		# connector_table_list = ['Connector_RPS2_SDS2_Channel1']
		
		##SDS2-RPS2
		comp_table_list=['Manual_Test','PS','Thermo_CSAM1','Thermo_CSAM2','Thermo_CSAM3','ASP_TC_CSAM1','ASP_TC_CSAM2','ASP_TC_CSAM3','Comparator_TC_CSAM1','Comparator_TC_CSAM2','Comparator_TC_CSAM3','PCSL_CSAM_RPS2_SDS2']
		connector_table_list = ['Connector_RPS2_SDS2_HER']
		
		##SDS2-AS
		# comp_table_list=['PCSL_CSAM_RPS2_SDS2','Manual_Test','PS','SCRAM_SW_SDS2_1A','SCRAM_SW_SDS2_1B','DSR_1','SCRAM_SW_SDS2_2A','SCRAM_SW_SDS2_2B','DSR_2','SCRAM_SW_SDS2_3A','SCRAM_SW_SDS2_3B','DSR_3']
		# connector_table_list = ['Connector_AS_SDS2']
		
		##SDS2
		# comp_table_list=['Thermo_CSAM1','Thermo_CSAM2','Thermo_CSAM3','ASP_TC_CSAM1','ASP_TC_CSAM2','ASP_TC_CSAM3','Comparator_TC_CSAM1','Comparator_TC_CSAM2','Comparator_TC_CSAM3','PCSL_CSAM_RPS2_SDS2','SCRAM_SW_SDS2_1A','SCRAM_SW_SDS2_1B','DSR_1','SCRAM_SW_SDS2_2A','SCRAM_SW_SDS2_2B','DSR_2','SCRAM_SW_SDS2_3A','SCRAM_SW_SDS2_3B','DSR_3','Manual_Test','PS']
		# connector_table_list = ['Connector_SDS2']
		# failgp = ['Manual_Test','PS','Thermo_CSAM1','Thermo_CSAM2','Thermo_CSAM3','ASP_TC_CSAM1','ASP_TC_CSAM2','ASP_TC_CSAM3','Comparator_TC_CSAM1','Comparator_TC_CSAM2','Comparator_TC_CSAM3','PCSL_CSAM_RPS2_SDS2','SCRAM_SW_SDS2_1A','SCRAM_SW_SDS2_1B','DSR_1','SCRAM_SW_SDS2_2A','SCRAM_SW_SDS2_2B','DSR_2','SCRAM_SW_SDS2_3A','SCRAM_SW_SDS2_3B','DSR_3']
		
		## Full SDS
		# comp_table_list=['NS_1XM','NS_1XN','NS_1YM','NS_1YN','NS_1ZM','NS_1ZN','EM_FM_1XA','EM_FM_1XB','EM_FM_1YA','EM_FM_1YB','EM_FM_1ZA','EM_FM_1ZB','ASP_NS_1XM','ASP_NS_1XN','ASP_NS_1YM','ASP_NS_1YN','ASP_NS_1ZM','ASP_NS_1ZN','OR_NS_1X','OR_NS_1Y','OR_NS_1Z','ASP_EMFM_1XA','ASP_EMFM_1XB','ASP_EMFM_1YA','ASP_EMFM_1YB','ASP_EMFM_1ZA','ASP_EMFM_1ZB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PbyQ_Compute_1YA','PbyQ_Compute_1YB','PbyQ_Compute_1ZA','PbyQ_Compute_1ZB','PQ_Comparator_1XA','PQ_Comparator_1XB','PQ_Comparator_1YA','PQ_Comparator_1YB','PQ_Comparator_1ZA','PQ_Comparator_1ZB','SLFIT_RPS_1','Manual_Test','PS','SCRAM_SW_SDS1_1A','SCRAM_SW_SDS1_1B','CSR_1','SCRAM_SW_SDS1_2A','SCRAM_SW_SDS1_2B','CSR_2','SCRAM_SW_SDS1_3A','SCRAM_SW_SDS1_3B','CSR_3','SCRAM_SW_SDS1_4A','SCRAM_SW_SDS1_4B','CSR_4','SCRAM_SW_SDS1_5A','SCRAM_SW_SDS1_5B','CSR_5','SCRAM_SW_SDS1_6A','SCRAM_SW_SDS1_6B','CSR_6','SCRAM_SW_SDS1_7A','SCRAM_SW_SDS1_7B','CSR_7','SCRAM_SW_SDS1_8A','SCRAM_SW_SDS1_8B','CSR_8','SCRAM_SW_SDS1_9A','SCRAM_SW_SDS1_9B','CSR_9','Thermo_CSAM1','Thermo_CSAM2','Thermo_CSAM3','ASP_TC_CSAM1','ASP_TC_CSAM2','ASP_TC_CSAM3','Comparator_TC_CSAM1','Comparator_TC_CSAM2','Comparator_TC_CSAM3','PCSL_CSAM_RPS2_SDS2','SCRAM_SW_SDS2_1A','SCRAM_SW_SDS2_1B','DSR_1','SCRAM_SW_SDS2_2A','SCRAM_SW_SDS2_2B','DSR_2','SCRAM_SW_SDS2_3A','SCRAM_SW_SDS2_3B','DSR_3']
		# connector_table_list = ['Connector_SDS_Full']	
		
		#comp_table_list = ['DND_1','DND_2','DND_3','DND_4','DND_5','DND_6','ASP_DND_1','ASP_DND_2','ASP_DND_3','ASP_DND_4','ASP_DND_5','ASP_DND_6','Manual_Test','Comparator_DND_1','Comparator_DND_2','Comparator_DND_3','Comparator_DND_4','Comparator_DND_5','Comparator_DND_6','SLFIT_1','SLFIT_2','SCRAM_SW_1A','SCRAM_SW_1B','PS','CSR_1']
		
		#comp_table_list =['2by3Vote_1','2by3Vote_2','Comparator_1','Comparator_2','Comparator_3','Comparator_4','Comparator_5','Comparator_6','CR','EM','ORGate','PS','Thermo_1','Thermo_2','Thermo_3','Thermo_4','Thermo_5','Thermo_6','ASP_1','ASP_2','ASP_3','ASP_4','ASP_5','ASP_6','Manual_Test']
		
	elif DSNstr == 'TestedSystemDB' or DSNstr == 'TestedSystemDBCopy1':
		comp_table_list = ['TestingSystem','VotingLogic_Tested','Manual_Test']
		connector_table_list = []
	elif DSNstr == 'DB4' or DSNstr == 'DB5':
		# comp_table_list = ['Component1','Result','Manual_Test']#
		# connector_table_list = ['Connector_One_Comp']
		# im.II = [[0,1]]
			
		# comp_table_list = ['Component1','Component2','Result']
		# connector_table_list = ['Connector_Two_Comp_Series']
		# im.II = [[0,2]]
		
		## Three component series
		# comp_table_list = ['Component1','Component2','Component3','Result']
		# connector_table_list = ['Connector_Three_Comp_Series']
		# im.II = [[0,3]]
		
		## Two components in parallel
		# comp_table_list = ['Component1','Component2','Result','Manual_Test']
		# connector_table_list = ['Connector_Two_Comp_Parallel']
		# im.II = [[0,2],[1,2]]
		
		## Three components in parallel
		# comp_table_list = ['Component1','Component2','Component3','Result',]
		# connector_table_list = ['Connector_Three_Comp_Parallel']
		# im.II = [[0,3],[1,3],[2,3]]
		
		## Four components in parallel
		# comp_table_list = ['Component1','Component2','Component3','Component4','Result',]
		# connector_table_list = ['Connector_Four_Comp_Parallel']
		# im.II = [[0,4],[1,4],[2,4],[3,4]]
		
		## Three componet Series-Parallel 
		# comp_table_list = ['Component1','Component2','Component3','Result']
		# connector_table_list = ['Connector_Three_Comp_Series_Parallel']
		# im.II = [[0,3]]

		## 2by3 Voting system
		comp_table_list = ['Component1','Component2','Component3','Result','2by3Vote']#Manual_Test'
		connector_table_list = ['Connector_2by3']
		im.II = [[0,3],[1,3],[2,3]]
		
		## Book Lewis Exaple 9.6. with  tau = 20 hrs
		# comp_table_list = ['Component1','Component2','Component3','Component4','Component5','Component6','Result','Manual_Test']
		# connector_table_list = ['Connector_Six_Comp_Parallel']
		# im.II = [[0,6],[1,6],[2,6],[3,6],[4,6],[5,6]]
		
		## Ten components system Vesely's, Lewis's
		# comp_table_list = ['Component1','Component2','Component3','Component4','Component5','Component6','Component7','Component8','Component9','Component10','Result','Manual_Test']
		# connector_table_list = ['Connector_10_Comp']
		
		
		# comp_table_list = []
		# connector_table_list = []
		# for row in cur.tables():
			#Since row is having list of both tables i.e. "SYSTEM(OS) TABLE" and "TABLE", IF statements is used in next line
			# if row[3]=='TABLE':
				# if raw_input('Is %s a component'%row[2])=='y':
					# comp_table_list.append(row[2])
				# elif raw_input('Is %s a connector'%row[2])=='y':
					# connector_table_list.append(row[2])
		# k = 0
		# for i in comp_table_list:
			# print i, k
			# k = k + 1
		# im.II = [[int(raw_input('Start=')),int(raw_input('End='))] for i in range(int(raw_input('number of [start,end] pairs')))]
	elif DSNstr == 'DB1':
		# comp_table_list  = ['PowerSupply','Valve1','Valve2','HX1','HX2','RPV']
		# connector_table_list = ['Connector']
		comp_table_list  = ['PowerSupply','AutoControl','Human_Action','Valve1', 'Valve2', 'HX1', 'HX2', 'Fuel' ]
		connector_table_list = ['Connector_DHR_Model']
	# k = 0
	# for i in comp_table_list:
		# print i, k
		# k = k + 1
	# im.II = [[int(raw_input('Start=')),int(raw_input('End='))] for i in range(int(raw_input('number of [start,end] pairs')))]
	
	im.exec_seq = comp_table_list
	
	#im.exec_seq =['NS_1XM','NS_1XN','ASP_NS_1XM','ASP_NS_1XN','OR_NS_1X','PbyQ_Compute_1XA','Manual_Test','PS']
	
	# im.exec_seq=['NS_1XM','NS_1XN','ASP_NS_1XM','ASP_NS_1XN','OR_NS_1X','EM_FM_1XA','ASP_EMFM_1XA','EM_FM_1XB','ASP_EMFM_1XB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PQ_Comparator_1XA','PQ_Comparator_1XB','SLFIT_RPS_1','Manual_Test','PS']
	#im.exec_seq=['NS_1XM','ASP_NS_1XM','NS_1XN','ASP_NS_1XN','OR_NS_1X','EM_FM_1XA','ASP_EMFM_1XA','EM_FM_1XB','ASP_EMFM_1XB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PQ_Comparator_1XA','PQ_Comparator_1XB','NS_1YM','ASP_NS_1YM','NS_1YN','ASP_NS_1YN','OR_NS_1Y','EM_FM_1YA','ASP_EMFM_1YA','EM_FM_1YB','ASP_EMFM_1YB','PbyQ_Compute_1YA','PQ_Comparator_1YA','PbyQ_Compute_1YB','PQ_Comparator_1YB','NS_1ZM','ASP_NS_1ZM','NS_1ZN','ASP_NS_1ZN','OR_NS_1Z','EM_FM_1ZA','ASP_EMFM_1ZA','EM_FM_1ZB','ASP_EMFM_1ZB','PbyQ_Compute_1ZA','PQ_Comparator_1ZA','PbyQ_Compute_1ZB','PQ_Comparator_1ZB','SLFIT_RPS_1','Manual_Test','PS']

	# im.exec_seq=['SLFIT_RPS_1','PS','SCRAM_SW_SDS1_1A','SCRAM_SW_SDS1_1B','CSR_1','SCRAM_SW_SDS1_2A','SCRAM_SW_SDS1_2B','CSR_2','SCRAM_SW_SDS1_3A','SCRAM_SW_SDS1_3B','CSR_3','SCRAM_SW_SDS1_4A','SCRAM_SW_SDS1_4B','CSR_4','SCRAM_SW_SDS1_5A','SCRAM_SW_SDS1_5B','CSR_5','SCRAM_SW_SDS1_6A','SCRAM_SW_SDS1_6B','CSR_6','SCRAM_SW_SDS1_7A','SCRAM_SW_SDS1_7B','CSR_7','SCRAM_SW_SDS1_8A','SCRAM_SW_SDS1_8B','CSR_8','SCRAM_SW_SDS1_9A','SCRAM_SW_SDS1_9B','CSR_9']
	#im.exec_seq=['NS_1XM','NS_1XN','NS_1YM','NS_1YN','NS_1ZM','NS_1ZN','EM_FM_1XA','EM_FM_1XB','EM_FM_1YA','EM_FM_1YB','EM_FM_1ZA','EM_FM_1ZB','ASP_NS_1XM','ASP_NS_1XN','ASP_NS_1YM','ASP_NS_1YN','ASP_NS_1ZM','ASP_NS_1ZN','OR_NS_1X','OR_NS_1Y','OR_NS_1Z','ASP_EMFM_1XA','ASP_EMFM_1XB','ASP_EMFM_1YA','ASP_EMFM_1YB','ASP_EMFM_1ZA','ASP_EMFM_1ZB','PbyQ_Compute_1XA','PbyQ_Compute_1XB','PbyQ_Compute_1YA','PbyQ_Compute_1YB','PbyQ_Compute_1ZA','PbyQ_Compute_1ZB','PQ_Comparator_1XA','PQ_Comparator_1XB','PQ_Comparator_1YA','PQ_Comparator_1YB','PQ_Comparator_1ZA','PQ_Comparator_1ZB','SLFIT_RPS_1','Manual_Test','PS']
	
	#im.exec_seq=['DND_1','DND_2','DND_3','DND_4','DND_5','DND_6','ASP_DND_1','ASP_DND_2','ASP_DND_3','ASP_DND_4','ASP_DND_5','ASP_DND_6','Comparator_DND_1','Comparator_DND_2','Comparator_DND_3','Comparator_DND_4','Comparator_DND_5','Comparator_DND_6','SLFIT_1','SLFIT_2','SCRAM_SW_1A','SCRAM_SW_1B','PS','CSR_1']
	#im.exec_seq=['PS','Thermo_1','Thermo_2','Thermo_3','Thermo_4','Thermo_5','Thermo_6','ASP_1','ASP_2','ASP_3','ASP_4','ASP_5','ASP_6','Comparator_1','Comparator_2','Comparator_3','Comparator_4','Comparator_5','Comparator_6','2by3Vote_1','2by3Vote_2','ORGate','EM','CR']
	
	###########
	## Components reading
	## Reading each component and converting database to dictionary of Python for faster processing
	main_tbl_list = {}
	for i in range(len(comp_table_list)):
		cur.execute(" SELECT *FROM %s "%(comp_table_list[i]))
		rows_ctd = cur.fetchall()
		att_val1 = []
		for j in rows_ctd:
			att_val1.append([j[1],j[3]])
		att_val1 = dict(att_val1)# returns :{att1: values1, att2:values2}
		main_tbl_list.update({comp_table_list[i]:att_val1})
	###########
	
	###########
	## Connector Tables reading
	## Reading each connector and converting database to dictionary of Python for faster processing
	connections_list = {}
	if len(connector_table_list) != 0:
		for i in range(len(connector_table_list)):
			cur.execute(" SELECT *FROM %s "%(connector_table_list[i]))
			rows=cur.fetchall()
			att_val1=[]
			for d in range(len(rows)):
				ex  = comp_table_list.index(rows[d][1])# from component index
				exa = rows[d][2]# from component parameter
				ey  = comp_table_list.index(rows[d][3])# to component index
				eya = rows[d][4]# to component parameter
				att_val1.append([ex,exa,ey,eya])
			connections_list.update({connector_table_list[i]:att_val1})
	cur.close()
	im.permanent_initial_value = main_tbl_list
	# im.failgpID = [[comp_table_list.index(failgp[i][j])for j in range(len(failgp[i]))] for i in range(len(failgp))]
	return [comp_table_list,main_tbl_list,connections_list];

###########
## python module __name__ testing code: dict_manipulation
if __name__ == "__main__":
	'''
	python dict_manipulation.py "TestedSystemDB" -fn "filename"
	python dict_manipulation.py -h
	python dict_manipulation.py -comp "Component"
	python dict_manipulation.py -conn "Connector"
	
	
	'''
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument("DSNstr",type=str, help='''DSN name of database (Mandatory)
	
	\n\n Available Options:-
	
	\n\n #'DB1'#'ShutdownSysRod1'#'TestedSystemDB'#'DB4'#''')	
	parser.add_argument("-n","--number", help="number")
	parser.add_argument("-fn","--filename", help="output filename")
	parser.add_argument("-comp","--component", type=str, help="display a component table")
	parser.add_argument("-conn", "--connector", help="display a connenctor table")
	
	args =  parser.parse_args()
	x = mainfunction2(args.DSNstr)
	if args.component:
		print(args.component, 'component is defined as below')
		print(x[1][args.component])
	elif args.connector:
		print(args.connector, 'connector is defined as below')
		print(x[2][args.connector])
	else:
		print(x)
	# args.number = int(args.number)
	if args.filename:
		file = open("%s.txt"%(args.filename),'w')
	else:
		file = open("%s.txt"%(args.DSNstr),'w')
	# file = open("%s_%d.txt"%(args.DSNstr,args.number),'w')
	file.write(str(x))
	file.close()
	# import sys
	# x = mainfunction(str(sys.argv[1]))
	# try:
		# sys.argv[2]
	# except NameError:
		# sys.argv[2] = 'all'
	
	# if str(sys.argv[2])!= str('all'):
		# if str(sys.argv[2])!= str('conn'):
			# print x[2][str(sys.argv[3])]
		# else:
			# print x[1][str(sys.argv[2])]
	# else:
		# print x
###########
## Dictionary as Values to Table Name
# x = [['name','darpan'],['customer','darpan'],['name','shukla'],['owner','shukla']]
# y = {'Table name':dict(x),'Table1':dict(x)}
# print y, y['Table1']['name']
###########

###########
## Addition of Dictionaries
## Note : recent redefinition or reassignment of values to a key is kept older is over written 
# x = [['name','darpan'],['customer','darpan'],['name','shukla'],['owner','shukla']]
# y = [['name','shukla'],['owner','shukla']]
# z=x+y
# z=dict(z)
# print z
###########

###########
## Example of Error: unhashable type list 
# x = [[['name','darpan'],['customer','darpan']],[['name','shukla'],['owner','shukla']]]
# x=dict(x)
# print x
###########


# print 'Dictionary',tables
# connector = 'Connector2'
# cur.execute("SELECT *FROM %s"%connector)
# rows=cur.fetchall()
# x=[[1,2],[3,4],[5,6]]
# print rows,dict(x)
# x=dict(x)
# x[3]=[i for i in range(10)]
# print x
