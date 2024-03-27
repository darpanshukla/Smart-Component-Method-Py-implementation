#!/usr/bin/python
import sys
import argparse
from generate_collapsed_model import generate_next_hierarchy
def pn_write(string):
	#print 'writing===>',string,
	if string[-1] != '\n':
		string += '\n'
	pn_file.write(string)
	#print 'done\n'
	return;
def gen_parameter_string(parameter):
	value = preemble[parameter]
	return_str = '\t'+parameter+' '+str(value)+'\n'
	return return_str;
def prepare_parameter(listofparameters):
	for i in listofparameters:
		pn_write(gen_parameter_string(i))
	return;		
def identify_places(component):
	listofplaces = []
	if int(temp[1][component]['Rel_Model']) == 3:
		listofplaces.append(component+'P1')
		listofplaces.append(component+'P0')	
	elif int(temp[1][component]['Rel_Model']) == 5:
		listofplaces.append(component+'P1')
		listofplaces.append(component+'P0')
		listofplaces.append(component+'P2')
	ccf = int(temp[1][component]['CCF'])
	if ccf > 0:
		for i in range(ccf):
			ccfid = int(temp[1][component]['CCF_ID%d'%(i+1)])
			if 'CCFG%d'%ccfid in listofCCFG:
				listofplaces.append('CCF'+str(ccfid)+component+'ON')
				listofCCFG['CCFG%d'%ccfid]['members'].append(component)
			else:
				listofCCFG['CCFG%d'%ccfid] = {'Repre':component,'members':[component]}
				listofCCFG['representative'].append(component)
	else:
		pass
	listofplaces.append(component+'PF')
	return listofplaces;
def construct_failure_tr(component,l):
	# failure transition
	transition_str       = 'T%s10:'%component
	transition_str      += 'rate:' + '%s '%(l)
	transition_str      += 'IN '   + '%s '%(temp[1][component]['Places'][0]) 
	transition_str      += 'OUT '  + '%s '%(temp[1][component]['Places'][1]) + '%s '%(temp[1][component]['Places'][-1])+ '\n'
	return transition_str;
def construct_CC_failure_tr(component,l,ccfid):
	# failure transition
	p1                   = ' %s'%temp[1][component]['Places'][0]
	p0                   = ' %s'%temp[1][component]['Places'][1]
	pf                   = ' %s'%temp[1][component]['Places'][-1]
	
	transition_str       = 'TCCF%d%s10:'%(ccfid,component)
	transition_str      += 'rate:' + '%s'%(l)
	transition_str      += ' IN'   + p1
	lsplace              = ''
	for i in listofCCFG['CCFG%d'%ccfid]['members'][1:]:
		lsplace         += ' CCF' + str(ccfid) + i         + 'ON'
		
	transition_str      += ' OUT' + p0         + pf        + lsplace + '\n'
	return transition_str;
def construct_CCF_effect(component,l,ccfid,relmodel):

	enforceplace         = ' CCF' + str(ccfid) + component + 'ON'
	p1                   = ' %s'%temp[1][component]['Places'][0]
	p0                   = ' %s'%temp[1][component]['Places'][1]
	pf                   = ' %s'%temp[1][component]['Places'][-1]
	
	if relmodel == 3:

		transition_str   = 'RESETCCF%d%s10:'%(ccfid,component)
		transition_str  += 'instant'
		transition_str  += ' IN'    + enforceplace + p1  + pf     + ':inh'
		transition_str  += ' OUT'   + p0           + pf  + '\n'
		
		transition_str1  = 'RESETCCF%d%s00:'%(ccfid,component)
		transition_str1 += 'instant '
		transition_str1 += ' IN'    + enforceplace + p1  + ':inh' + pf 
		transition_str1 += ' OUT'   + pf           + '\n'
		
		transitions      = [ transition_str, transition_str1 ] 

	elif relmodel == 5:
		
		p2               = ' %s'%temp[1][component]['Places'][2]
		
		transition_str   = 'RESETCCF%d%s10:'%(ccfid,component)
		transition_str  += 'instant'
		transition_str  += ' IN'    + enforceplace + p1 + pf     + ':inh'
		transition_str  += ' OUT'   + p0           + pf + '\n'
		
		transition_str1  = 'RESETCCF%d%s00:'%(ccfid,component)
		transition_str1 += 'instant'
		transition_str1 += ' IN'    + enforceplace + p1 + ':inh' + pf + p0
		transition_str1 += ' OUT'   + pf           + p0 + '\n'
		
		transition_str2  = 'RESETCCF%d%s20:'%(ccfid,component)
		transition_str2 += 'instant'
		transition_str2 += ' IN'    + enforceplace + p1 + ':inh' + p2 + ':inh' + pf
		transition_str2 += ' OUT'   + pf           + p0
		transition_str2 += ' RESET' + p2           + '\n'
		
		transitions      = [ transition_str, transition_str1, transition_str2 ] 
	return transitions;
def construct_repair_tr(component):
	# repair transition
	transition_str = 'T%s01:'%component
	transition_str += 'rate:' + '%s '%(temp[1][component]['Repair Rate'])
	transition_str += 'IN '   + '%s '%(temp[1][component]['Places'][1])   + '%s '%(temp[1][component]['Places'][-1])
	transition_str += 'OUT '  + '%s '%(temp[1][component]['Places'][0])   + '\n'
	return transition_str;
def construct_test_tr(component):
	transition_str = 'T%s02:'%component
	transition_str += 'cyclic:' + '%s:'%(temp[1][component]['TestTime'])  + '0 '#'%d '%(temp[1][component]['TestOffset'])
	transition_str += 'IN '     + '%s '%(temp[1][component]['Places'][1]) 
	transition_str += 'OUT '    + '%s '%(temp[1][component]['Places'][2]) + '\n'
	return transition_str;	
def construct_test_repair_tr(component):
	# test and then repair transition
	transition_str = 'T%s21:'%component
	transition_str += 'rate:' + '%s '%(temp[1][component]['Repair Rate'])
	transition_str += 'IN '   + '%s '%(temp[1][component]['Places'][2])   + '%s '%(temp[1][component]['Places'][-1])
	transition_str += 'OUT '  + '%s '%(temp[1][component]['Places'][0])   + '\n'
	return transition_str;
def identify_transition(component):
	listoftransition = []
	## CCF effects and transitions
	ccf      = int(temp[1][component]['CCF'])
	relmodel = int(temp[1][component]['Rel_Model'])
	
	if ccf > 0:
		if component in listofCCFG['representative']:
			l1            = float(temp[1][component]['Failure Rate'])
			beta          = 0
			
			for i in range(ccf):
				ccfid     = int(temp[1][component]['CCF_ID%d'%(i+1)])
				if listofCCFG['CCFG%d'%ccfid]['Repre'] == component:
					beta1 = float(temp[1][component]['Beta%d'%(i+1)])/100.0
					l     = beta1 * l1
					beta += beta1
					listoftransition.append( construct_CC_failure_tr( component, l, ccfid ) )
			l = beta * l1
		else:
			l = float(temp[1][component]['Failure Rate'])
			for i in range(ccf):
				ccfid             = int(temp[1][component]['CCF_ID%d'%(i+1)])
				listoftransition += construct_CCF_effect( component, l, ccfid, relmodel )
	else:
		l = float(temp[1][component]['Failure Rate'])
		
	if relmodel == 3:
		listoftransition.append( construct_failure_tr(  component, l ))
		listoftransition.append( construct_repair_tr(      component ))
	elif relmodel == 5:
		listoftransition.append( construct_failure_tr(  component, l ))
		listoftransition.append( construct_test_tr(        component ))
		listoftransition.append( construct_test_repair_tr( component ))

	return listoftransition;
	
def generate_hl_series_transitions(pflist, placename, hl, id ):
	listoftransition = []
	#failure counnting up
	for i in range(len(pflist)):
		transitionstr  = 'THL%dI%di%d:instant'%(hl,id,i)
		transitionstr += ' IN'  + ' ' + pflist[i] + ' ' + placename + ':inh'
		transitionstr += ' OUT' + ' ' + pflist[i] + ' ' + placename + '\n'
		listoftransition.append(transitionstr)
		transitionstr  = ''
	#repair counting down
	transitionstr      = 'TRHL%dI%di%d:instant'%(hl,id,i)
	transitionstr     += ' IN'
	for j in range(len(pflist)):
		transitionstr += ' ' + pflist[j] + ':inh'
	transitionstr     += ' ' + placename
	listoftransition.append(transitionstr)
	return listoftransition;
	
def generate_hl_series_traditional_model( listofcid, complist, placename, hl, id ):
	pflist = []
	for i in listofcid:
		# gatherig indicator places
		pflist.append( temp[1][complist[i]]['Places'][-1] )
	transitions = generate_hl_series_transitions( pflist, placename, hl, id )
	return transitions;

def make_place_transition_series_connections(se_connection, compnamelist, lsplaces, hl ):
	transitionlist = []
	for i in range(len(se_connection)):
		n = len(se_connection[i])
		if n > 1:
			placename   = 'HLS%dID%d'%( hl, i )
			lsplaces[hl].append( placename )
			transition = generate_hl_series_traditional_model( se_connection[i], compnamelist, placename, hl, i ) 
			for j in transition:
				transitionlist.append(j)
		else:
			pass	
	return [ lsplaces, transitionlist ];
	
def make_up_transition( inputpl, spplace, gcplace ):
	trnname  = gcplace+'UP'+inputpl
	trn_str  = trnname + ':instant'
	trn_str += ' IN'  + ' ' + inputpl + ' ' + spplace + ':inh'
	trn_str += ' OUT' + ' ' + inputpl + ' ' + spplace + ' '    + gcplace + '\n'	
	return trn_str;
	
def make_down_transition( inputpl, spplace, gcplace ):
	trnname  = gcplace +'DOWN'      + inputpl
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + inputpl + ':inh ' + spplace + ' ' + gcplace
	trn_str += '\n'
	return trn_str;
	
def general_k_n_place_transition( k, se_connection, slist, compnamelist, lsplaces, hl, pid ):
	placelist      = []
	transitionlist = []
	gcplace        = 'GCount%dI%d'%( hl, pid )
	lsplaces[hl].append( gcplace )
	for i in range( len( slist ) ):
		n   =  len( se_connection[ slist[ i ] ] )
		
		## identify the input place 
		if n > 1:
			ip         = 'HLS%dID%d'%(  hl, slist[i] )
		elif n == 1:
			if hl == 1:
				ip     = compnamelist[  se_connection[slist[i]][0]]+'PF'
			else:
				ip     = 'HLP%dID%d'%(  hl, slist[i] )
				lsplaces[hl].append(    ip           )
		## semaphore place
		spplace        = 'SP%dI%di%d'%( hl, pid, i   )
		lsplaces[hl].append(   spplace )
		## up and down transition generations for counting
		transitionlist.append( make_up_transition(   ip, spplace, gcplace ) )
		transitionlist.append( make_down_transition( ip, spplace, gcplace ) )
	
	knsysplace = 'knSYS'   + gcplace
	lsplaces[hl].append( knsysplace )
	## k-out-of-n decision transition
	trnname  = 'TknUP' + knsysplace
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + gcplace + ':%d '%k     + knsysplace + ':inh'
	trn_str += ' OUT'  + ' '        + gcplace + ':%d '%k     + knsysplace + '\n'
	transitionlist.append( trn_str )
	trnname  = 'TknDN' + knsysplace
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + gcplace + ':inh:%d '%k + knsysplace
	trn_str += '\n'
	transitionlist.append( trn_str )
	return [ lsplaces, transitionlist ];
	
def two_place_series( p1, p2, sysplace ):
	transitionlist = []
	
	trnname  = 'TsysUP1' + sysplace
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + p1 + ' ' + sysplace + ':inh' 
	trn_str += ' OUT'  + ' '        + p1 + ' ' + sysplace + '\n'
	transitionlist.append( trn_str )
	
	trnname  = 'TsysUP2' + sysplace
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + p2 + ' ' + sysplace + ':inh' 
	trn_str += ' OUT'  + ' '        + p2 + ' ' + sysplace + '\n'
	transitionlist.append( trn_str )
	
	trnname  = 'TsysDOWN2' + sysplace
	trn_str  = trnname + ':instant'
	trn_str += ' IN'   + ' '        + p1 + ':inh ' + p2 + ':inh ' + sysplace 
	trn_str += '\n'
	transitionlist.append( trn_str )
	
	return transitionlist;
	
def make_place_transition_parallel_connections( se_connection, para_connection, compnamelist, lsplaces, hl ):
	lstransitions = []
	for i in range(len(para_connection)):
		
		try:
			k = int(temp[1][compnamelist[para_connection[i][1]]]['Logic'])
		except:
			k = len( para_connection[i][0] )
		[ lsplaces, transitions ] = general_k_n_place_transition( k, se_connection,  para_connection[i][0], compnamelist, lsplaces, hl, i )
		
		## Place for the parallel collapse
		if hl == 1:
			PCcompplace = temp[ 1 ][ compnamelist[ para_connection[i][1] ]]['Places'][-1]
		else:	
			PCcompplace = 'PCc%dI%d'%(hl,i) + temp[ 1 ][ compnamelist[ para_connection[i][1] ]]['Places'][-1]	
			lsplaces[hl].append(        PCcompplace                        )
		PCplace = 'PCc%dI%d'%( hl,                                       i )
		trn     = two_place_series( PCcompplace, lsplaces[hl][-1], PCplace )
		lsplaces[hl].append(        PCplace                                )
		for j in range( len(        trn                                   )):
			transitions.append(   trn[j]                                 )
		for j in range(len(transitions)):
			lstransitions.append(transitions[j])
	return [ lsplaces, lstransitions ];
def identify_places_transition( se_connection, para_connection, lsplaces, hl, compnamelist ):
	
	[ lsplaces, stransitions ] = make_place_transition_series_connections(   se_connection,                  compnamelist, lsplaces, hl ) 
	[ lsplaces, ptransitions ] = make_place_transition_parallel_connections( se_connection, para_connection, compnamelist, lsplaces, hl ) 
	tlist  = stransitions + ptransitions
	return [ lsplaces, tlist ];
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("DSNstr",type=str, help='''DSN name of database (Mandatory)''')
	args =  parser.parse_args()

	###############################################
	###############################################
	###############################################
	###############################################

	## Initialize output file

	pn_file = open('%s.mpn'%(args.DSNstr),'w')
	print("""Following will be written to the MPN input file
	|===========================|
		1 Petri Net parameters
		2 Run parameters
		3 Petri net
		4 PN Places
		5 PN Transitions
	|===========================|
	""")
	preemble = {'name':'PN_%s'%(args.DSNstr), 'units':'hrs', 'runMode':'schedule', 'visualise':'png', 'dot':'False', 'maxClock':1e14, 'maxSteps': 1e5, 'history': 'False', 'analysisStep':1}
	writing_sequence = ['name','units','runMode','visualise','dot','maxClock','maxSteps','history','analysisStep']

	inistring = "# Petri Net Parameters\n"
	pn_write( inistring )
	prepare_parameter( writing_sequence[ 0 : 5 ] )

	inistring = "# Run parameters\n"
	pn_write(inistring)
	prepare_parameter(writing_sequence[5:])

	######################=============================####################

	outfile = open("%s.txt"%(args.DSNstr),'r')
	line    = outfile.readlines()
	outfile.close()
	temp    = eval(line[0])

	## temp has the following: sequence of simulation, component data and connector

	## Collection of all the nodes:

	## 1) identify places for all the components defined in temp[1] with sequence given in temp[0]

	listofCCFG       = {'representative':[]}

	## Writing output file

	inistring = "# Build Petri net\n"
	pn_write(inistring)
	inistring = "Places\n"
	pn_write(inistring)


	listofplaces = {0:[]}
	for i in temp[0]:
		# Identifying places based on the assigned component model
		places_list          = identify_places( i )
		temp[1][i]['Places'] = places_list
		for j in range(len(places_list)):
			listofplaces[0].append( places_list[j] )
			if j == 0:# Intial value of token is 1 for the working place
				pn_write('\t' + places_list[j] + ' 1\n')
			else:
				pn_write('\t' + places_list[j] + '\n')

	lsoftransition = {0:[]}
	for i in temp[0]:
		tr_list                   = identify_transition(i)
		temp[1][i]['Transitions'] = tr_list
		for j in range(len(tr_list)):
			lsoftransition[0].append( tr_list[j] )

	# print '\n\n'*2,'List of places','\n\n', listofplaces[0],'\n\n'*2, 'List of transitions','\n\n', lsoftransition[0]
		
	
	thl                 = 6
	seq                 = [ i for i in range( len( temp[0] )) ]
	
	branches            = temp[2]['Connector']
	series_connection   = {0:{}}
	parallel_connection = {0:{}}
	print(seq, len(seq),'\n\n', 'Number of branches', len(branches))
	
	for i in range( 1, thl ):
		
		[seq, branches, series_connection[i], parallel_connection[i] ] = generate_next_hierarchy( seq, branches )
		print('*'*40,'\n\n Output for Hierarchy Level',i, '\n', '*'*40, '\n\n')
		print('*'*40, seq, len(seq), '\n\nSeries', series_connection[i], len(series_connection[i]), '\n\nParallel', parallel_connection[i],len(parallel_connection[i]), '\n\nBranches', branches, len(branches))
		listofplaces[i]   = []
		lsoftransition[i] = []
		[ listofplaces, lsoftransition[i] ] = identify_places_transition( series_connection[i], parallel_connection[i], listofplaces, i, temp[0] )

	for i in range(1, thl ):
		inistring = "# Places for Hierarchy %d\n"%i
		pn_write(inistring)
		for j in range(len(listofplaces[i])):
			pn_write('\t' + listofplaces[i][j] + '\n')
	inistring = "Transitions\n"
	pn_write(inistring)
	

	for i in range( thl ):
		inistring = "# Transitions for Hierarchy %d\n"%i
		pn_write(inistring)
		for j in range(len(lsoftransition[i])):
			pn_write('\t' + lsoftransition[i][j])