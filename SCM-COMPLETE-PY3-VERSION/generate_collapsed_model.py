#!/usr/bin/python
import sys
import argparse
from copy import deepcopy
	
def has_n_in( id, links ):
	'''
	Returns number of input links coming to id
	'''
	linkin = 0
	for l in links:
		if int(l[2]) == id:
			linkin += 1
	return linkin;
	
def has_n_in_link( id, links ):
	'''
	Returns list of input links coming to id
	'''
	list_linkin = []
	for l in links:
		if int(l[2]) == id:
			list_linkin.append(l)
	return list_linkin;

def has_n_out( id, links ):
	'''
	Returns number of output links coming out of id
	'''
	linkout = 0
	for l in links:
		if int(l[0]) == id:
			linkout += 1
	return linkout;
def has_n_out_link( id, links ):
	'''
	Returns list of input links coming out of id
	'''
	list_linkout = []
	for l in links:
		if int(l[0]) == id:
			list_linkout.append(l)
	return list_linkout;
def move_forward(id, links):
	for l in links:
		if int(l[0]) == id:
			id2 = int(l[2])
	return id2
def generate_series_hierarchy( id, links ):
	if isinstance( id, list ):
		entry = id
		id    = id[ -1 ]
	else:
		entry = [ id, ]
	while(1):
		lout = has_n_out( id,            links )
		if lout != 0:
			if lout == 1:
				## Move forward
				id2 = move_forward( id,  links )
				lin = has_n_in(     id2, links )
				if lin > 1:
					break
				elif lin == 1:
					entry.append(  id2  )
					id = deepcopy( id2  )
			elif lout > 1:
				break
		else:
			break
	return entry
def generate_parallel_hierarchy( idlist1, series_connection, links ):
	'''
	inputs: [ series connection list ] and [ links ]
	output: [ [list of incoming series connection], component ]
	'''
	parallel_connection = [ ]
	for i in idlist1:
		temp1 = []
		if has_n_in(i,links) > 1:
			ls = has_n_in_link(i,links)
			for j in ls:
				for k in range(len(series_connection)):
					if j[0] == series_connection[k][-1]:
						temp1.append(k)
		if len( temp1 ) > 0:
			parallel_connection.append( [ temp1, i ] )
	return parallel_connection;
def remove_duplicate(links):
	## remove duplicates
	for i in range(len(links)):
		links[i] = str(links[i])
	links = list(dict.fromkeys(links))
	links = [ eval(links[i]) for i in range(len(links))]
	return links;
def del_connections( listoflinkid, links ):
	listoflinkid.sort(reverse=True)
	for i in listoflinkid:
		print(links[i])
		del links[i]
	return links;
def del_connections_with_same_io( links ):
	linkdellist = []
	for i in range(len(links)):
		if int(links[i][0]) == int(links[i][2]):
			linkdellist.append(i)
	links = del_connections(linkdellist, links)
	return links;
	
def process_d_generated_hierarchy(idlist1, links, series_connection, parallel_connection ):
	'''
	Inputs: links, series connections, parallel connections
	Outputs: Sequence, Series and parallelly collapsed links
	'''
	sel_list    = [ i for i in range(len(series_connection)) ]
	linkdellist = []
	iddellist   = []
	
	## Series collapse
	for i in range(len(series_connection)):# for loop over the list of series connections
		if len(series_connection[i]) > 1:# check the length of the series connection if it is > 1 then do collapse
			# print 'series collapse for', series_connection[i]
			for k in range(len(links)):# for loop over the links to be modified
				# k is the id of branch number
				if ( links[k][0] in series_connection[i][:-1] ) and ( links[k][2] in series_connection[i][1:] ):
					# Series collapse for intermediate
					linkdellist.append(k)
				if links[k][0] == series_connection[i][-1]:
					# series collapse at end
					links[k][0] = series_connection[i][0]
			for k in range(1,len(series_connection[i])):# for loop over the component ids of the series connection to delete the comp ids
				if series_connection[i][k] not in iddellist:
					iddellist.append(series_connection[i][k])
		else:
			pass
	# print 'Link delete list=',linkdellist
	links       = del_connections( linkdellist, links )
	linkdellist = []
	
	for i in iddellist:
		if i in idlist1:
			idlist1.remove(i)
	
	## Parallel collapse
	# Here we collapsing the parallel connection from back to front
	for i in range(len(parallel_connection)):
		# for loop over all the parallel connection
		llout = []
		for j in range(len(parallel_connection[i][0])):
			# j is id number for the incoming series connections to the component [i][1]
			# for loop is for identifying the number of out-going link from the input IP of the parallel circuit
			llout.append(has_n_out(series_connection[parallel_connection[i][0][j]][0],links))
		# print llout
		if llout.count(1) == len(llout):
			# condition of parallel collapse is that if all the input series inputs must have only one out-going link that and that too to the current voter i.e. parallel_connection[i][1]
			# print 'Parallel collapsing for', parallel_connection[i]
			## Now parallel collapsing
			for j in parallel_connection[i][0]:
				# for loop over all the series inputs IPs
				for k in range(len(links)):
					# for loop over all the links to process the links, where, k is link id, j is series input id
					
					# parallel collapse at the front side
					if links[k][2]  == series_connection[j][0]:
						links[k][2]  = parallel_connection[i][1]

					# parallel collapse for the ith component with its input id number in the series connection
					if (links[k][0] == series_connection[j][0]) and (links[k][2] == parallel_connection[i][1]):
						linkdellist.append(k)
						if links[k][0] in idlist1:
							idlist1.remove(links[k][0])
		else:
			pass
	links = del_connections( linkdellist, links )
	links = remove_duplicate(             links )
		
	return  [ idlist1, links ];
	
def generate_next_hierarchy( idlist, links ):
	
	idlist1        = deepcopy( idlist )
	branches       = deepcopy( links  )
	
	#########################################################
	## Series collapse
	#########################################################
	
	series_hierarchy = []
	id               = idlist[0]
	idlist.remove( id )
	while len(idlist) != 0:
		entry1  = generate_series_hierarchy( id, branches )
		series_hierarchy.append( entry1 )
		
		if len(entry1) > 1:
			for i in entry1[1:]:
				if i in idlist:
					idlist.remove(i)
		
		if len( idlist ) != 0:
			id = idlist[ 0 ]
			idlist.remove(id)
		else:
			break

	#########################################################
	## Parallel collapse
	#########################################################

	parallel_hierarchy = []
	parallel_conn = []
	if len( series_hierarchy ) != 0:
		parallel_conn = generate_parallel_hierarchy( idlist1, series_hierarchy, branches )

	#########################################################
	## Processing the branches and id list
	#########################################################

	[ idlist2, branches1 ] = process_d_generated_hierarchy( idlist1, branches, series_hierarchy, parallel_conn )

	#########################################################	
	return [ idlist2, branches1, series_hierarchy, parallel_conn ];
	
if __name__ == "__main__":

	parser         = argparse.ArgumentParser()
	parser.add_argument( "DSNstr", type=str, help='''DSN name of database (Mandatory)''' )
	args           = parser.parse_args()
	outfile        = open( "%s.txt"%(args.DSNstr), 'r' )
	line           = outfile.readlines()
	outfile.close()
	temp           = eval( line[0] )
	
	seq            = temp[0]
	idlist         = [i for i in range(len(temp[0]))]
	idlist2        = deepcopy(idlist)
	branches       = temp[2]['Connector']
	
	#########################################################
	## Series collapse
	#########################################################
	series_hierarchy = []
	id               = idlist[0]
	idlist.remove( id )
	while len( idlist ) != 0:
		entry1 = generate_series_hierarchy( id, branches )
		series_hierarchy.append( entry1 )
		id = idlist[ 0 ]
		idlist.remove( id )

	#########################################################
	## Parallel collapse
	#########################################################

	parallel_hierarchy = []
	if len( series_hierarchy ) != 0:
		parallel_conn = generate_parallel_hierarchy(idlist2, series_hierarchy, branches )

	#########################################################

	print(series_hierarchy, parallel_conn)
	[idlist2, branches1]  = process_d_generated_hierarchy(idlist2, branches, series_hierarchy, parallel_conn)
	
	#########################################################

	
	
	print('\n========================+++++++++++++++++==============='*10)
	print(' Second iteration begins', '\n'*5)
	idlist    = deepcopy(idlist2)
	branches  = deepcopy(branches1)
	print(idlist,branches)
	#########################################################
	## Series collapse
	#########################################################
	series_hierarchy = []
	id               = idlist[0]
	idlist.remove( id )
	while len( idlist ) != 0:
		entry1 = generate_series_hierarchy( id, branches )
		series_hierarchy.append( entry1 )
		id = idlist[ 0 ]
		idlist.remove( id )

	#########################################################
	## Parallel collapse
	#########################################################
	
	
	if len( series_hierarchy ) != 0:
		parallel_conn = generate_parallel_hierarchy( idlist2, series_hierarchy, branches )
	#########################################################
	print(series_hierarchy, parallel_conn)

	[idlist2, branches1]  = process_d_generated_hierarchy( idlist2, branches, series_hierarchy, parallel_conn )
	
	print('\n========================+++++++++++++++++==============='*10)
	print(' Third iteration begins', '\n'*5)
	idlist    = deepcopy(idlist2) 
	branches  = deepcopy(branches1)
	print(idlist,branches)
	#########################################################
	## Series collapse
	#########################################################
	series_hierarchy = []
	id               = idlist[0]
	idlist.remove( id )
	while len( idlist ) != 0:
		entry1 = generate_series_hierarchy( id, branches )
		series_hierarchy.append( entry1 )
		id = idlist[ 0 ]
		idlist.remove( id )

	#########################################################
	## Parallel collapse
	#########################################################
	
	
	if len( series_hierarchy ) != 0:
		parallel_conn = generate_parallel_hierarchy( idlist2, series_hierarchy, branches )
	#########################################################
	print(series_hierarchy, parallel_conn)
	[ idlist2, branches1 ]  = process_d_generated_hierarchy( idlist2, branches, series_hierarchy, parallel_conn )