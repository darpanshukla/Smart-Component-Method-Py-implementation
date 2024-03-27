#!/usr/bin/python
import sys
import argparse
from copy import deepcopy

listofstart    = []
listofinward   = []
listofoutward  = []
listofend      = []
series_hierarchy = []

def number_of_start_stop_entry(seq,links):
	
	for compid in range(len(seq)):
		## Finding starting components
		linkin = 0
		for l in links:
			if int(l[2]) == compid:
				linkin += 1
		#print '#incoming links', linkin
		if linkin == 0:
			listofstart.append(compid)
		
		listofinward.append(linkin)
			
		## Finding ending components
		linkout = 0
		for l in links:
			if int(l[0]) == compid:
				linkout += 1
		if linkout == 0:
			listofend.append(compid)
		listofoutward.append(linkout)
	return;
	
def has_start( id, links ):
	linkin = 0
	for l in links:
		if int(l[2]) == id:
			linkin += 1
	return linkin;
def whether_end( id, links ):
	linkout = 0
	for l in links:
		if int(l[0]) == id:
			linkout += 1
	return linkout;
def move_forward(id, links):
	for l in links:
		if int(l[0]) == id:
			id2 = int(l[2])
	return id2
def generate_series_hierarchy( id, links ):
	if isinstance(id, list):
		entry = id
		id    = id[-1]
	else:
		entry = [id,]
	while(1):
		lout = whether_end(id, links)
		if lout != 0:##can be avoided with the item in listofend
			if lout == 1:
				## Move forward
				id2 = move_forward(id, links)
				lin = has_start(id2, links)
				if lin > 1:
					break
				else:
					entry.append(id2)
					id  = deepcopy(id2)
					idlist.remove(id)
			elif lout > 1:
				break
		else:
			break
	return entry
def generate_parallel_hierarchy( series_connection, links):
	comingfrom_goingto = []
	for serially_reduced in series_connection:
		comingfrom_goingto.append([[],[]])
		for i in links:
			## enlisting the incoming nodes
			if i[2] == serially_reduced[0]:
				comingfrom_goingto[-1][0].append( i[0] )
			else:
				pass
			## enlisting the outgoing nodes
			if i[0] == serially_reduced[-1]:
				comingfrom_goingto[-1][1].append( i[2] )
			else:
				pass
	
	cfgt = deepcopy( comingfrom_goingto )
	
	parallel_connections = [ [] for i in range( nofcomp ) ]
	for i in range( nofcomp ):
		lin = has_start( i, links )
		if lin > 1:
			for j in range(len(series_connection)):
				if i in cfgt[j][1]:
					parallel_connections[i].append(j)
					cfgt[j][1].remove(i)
		else:
			pass	
	
	return [ comingfrom_goingto, parallel_connections ];
def generate_next_hierarchy( seq, links ):	
	
	number_of_start_stop_entry( seq, links )
	
	global idlist         
	idlist = [ i for i in range( len( seq ) ) ]
	id             = idlist[ 0 ]
	idlist.remove( id )
	while len( idlist ) != 0:
		entry1 = generate_series_hierarchy( id, links )
		series_hierarchy.append( entry1 )
		id = idlist[ 0 ]
		idlist.remove( id )
	if len( series_hierarchy ) != 0:
		[parallel_hierarchy, parallel_conn] = generate_parallel_hierarchy( series_hierarchy, links )
	return series_hierarchy, parallel_conn;
def idlist_remove(i, idlists1, idlistp1):
	if i in idlists1:
		idlists1.remove(i)
	if i in idlistp1:
		idlistp1.remove(i)
	return [idlists1,idlistp1];
def process_d_generated_hierarchy( links, series_connection, parallel_connection ):
	'''
	Inputs: links, series connections, parallel connections
	Outputs: Sequence, Series and parallelly collapsed links
	'''
	branches  = deepcopy(links)
	sel_list  = [ i for i in range(len(series_connection))]
	idlistp   = []
	dellist1  = []
	dellist2  = []
	## Series collapse
	for i in range(len(series_connection)):
		if len(series_connection[i]) > 1:
			j    = series_connection[i]
			print '\n\nSeries collapse is in progress for ID:', i, 'series_connection:', j
			for k in range(len(links)):
				# k is the id of branch number 
				if ( links[k][0] in j[:-1] ) and ( links[k][2] in j[1:] ):
					# Series collapse for intermediate branches
					dellist1.append(k)
					print 'deleting links:',links[k]
				if links[k][2] == j[0]:
					# series collapse at start
					print branches[k],'->',
					branches[k][2] = i
					print k,branches[k],'series collapse at start'
				if links[k][0] == j[-1]:
					# series collapse at end
					print branches[k],'->',
					branches[k][0] = i
					print k,branches[k],'series collapse at end'
	# print 'branch delete list for the series connections', dellist1
	## Parallel collapse
	pid = -1
	for i in range(len(parallel_connection)):
		# i is the id number of the component
		if len(parallel_connection[i]) > 1:
			pid +=  1
			idlistp.append(pid)
			print '\n\nParallel collapse for component id:', temp[0][i], 'pid:', pid, parallel_connection[i]
			for j in parallel_connection[i]:
				# j is id number for the incoming series connections to the component i
				print 'input:', j, ' which is a series connection of:', series_connection[j]
				for k in range( len(links) ):
					# k is the id of branch number 
					if (links[k][0] == series_connection[j][-1]) and (links[k][2] == i):
						# parallel collapse for the ith component with its input id number in the series connection 
						dellist2.append( k )
						print 'deleting link k:', k, links[k]
					if links[k][2] == series_connection[j][0]:
						# parallel contration at the front side
						print branches[k],'->',
						branches[k][2] = pid
						print k,branches[k],'parallel collapse at front'
			for k in range( len(links) ):
				if links[k][0] == i:
					# parallel contration at the back side
					print branches[k],'->',
					branches[k][0] = pid
					print k,branches[k],'parallel collapse at back'
	# print 'branch delete list for the parallel connectoins', dellist2
	dellist = dellist1 + dellist2
	
	dellist.sort( reverse = True )
	for i in dellist:
		print 'deleting branch k=%d'%i, links[i], '--->', branches[i]
		
		# [idlists,idlistp] = idlist_remove(branches[i][0],idlists,idlistp)
		[[],idlistp] = idlist_remove( branches[i][0], [], idlistp )
		[[],idlistp] = idlist_remove( branches[i][2], [], idlistp )
		
		del branches[i]
	
	## remove duplicates
	for i in range(len(branches)):
		branches[i] = str(branches[i])
	branches = list(dict.fromkeys(branches))
	branches = [ eval(branches[i]) for i in range(len(branches))]
	
	return idlistp , branches;
	
if __name__ == "__main__":

	parser         = argparse.ArgumentParser()
	parser.add_argument( "DSNstr", type=str, help='''DSN name of database (Mandatory)''' )
	args           = parser.parse_args()
	outfile        = open( "%s.txt"%(args.DSNstr), 'r' )
	line           = outfile.readlines()
	outfile.close()
	temp           = eval( line[0] )
	
	seq            = temp[0]
	print seq
	idlist         = [i for i in range(len(temp[0]))]
	branches       = temp[2]['Connector_SDS1']
	nofcomp        = len(temp[0])
	
	listofstart    = []
	listofinward   = []
	listofoutward  = []
	listofend      = []
	number_of_start_stop_entry( seq, branches )
	# print listofstart,listofend
	# print 'Starting points'
	# for i in listofstart:
		# print temp[0][i]
	# print 'Ending points'
	# for i in listofend:
		# print temp[0][i]

	#########################################################
	## Series collapse
	#########################################################
	series_hierarchy = []
	id               = idlist[0]
	idlist.remove( id )
	while len( idlist ) != 0:
		# print 'component',id,'is connected in series with',
		entry1 = generate_series_hierarchy( id, branches )
		# print entry1
		series_hierarchy.append( entry1 )
		id = idlist[ 0 ]
		idlist.remove( id )

	#########################################################

	print series_hierarchy, len(series_hierarchy)
	# series_hierarchy_name = []
	# for i in range(len(series_hierarchy)):
		# series_hierarchy_name.append([])
		# for j in series_hierarchy[i]:
			# series_hierarchy_name[-1].append(temp[0][j])
		# print i, series_hierarchy_name[i]

	#########################################################
	## Parallel collapse
	#########################################################

	parallel_hierarchy = []
	if len( series_hierarchy ) != 0:
		[ parallel_hierarchy, parallel_conn ] = generate_parallel_hierarchy( series_hierarchy, branches )

	#########################################################

	print parallel_conn, len(parallel_conn)

	# print '\n\n%20s\t->\t%30s\t->\t%20s'%('Coming from', ' Series connection ', ' Going to ')
	# for i in range(len(series_hierarchy)):
		# if listofinward[series_hierarchy[i][0]] != 0:
			# for k in range(listofoutward[series_hierarchy[i][-1]]):
				# for j in range(listofinward[series_hierarchy[i][0]]):
					# print '%20s\t->\t%30s%d\t->\t%20s'%( seq[parallel_hierarchy[i][0][j]], str(series_hierarchy_name[i]), i, seq[parallel_hierarchy[i][1][k]])
		# else:
			# for k in range(listofoutward[series_hierarchy[i][-1]]):
				# print '%20s\t->\t%30s%d\t->\t%20s'%( 'OOO-start--->', str(series_hierarchy_name[i]), i, seq[parallel_hierarchy[i][1][k]])
	# print idlist
	idlist         = [i for i in range(len(seq))]
	# print branches, len(branches),'\n'*5
	# for i in range(len(seq)):
		# for j in parallel_conn[i]:
			# print '%d\t%d\t%s\t->%20s'%(i,j,str(parallel_conn[i]),seq[i])
	
	[idlist1, branches1]  = process_d_generated_hierarchy( branches, series_hierarchy, parallel_conn)
	print idlist1, branches1
	