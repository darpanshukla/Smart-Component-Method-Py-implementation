#!/usr/bin/python
import os
import __init__ as im

def init_counters():	
	'''
	##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
			Arrays for transient estimates for Mission time model
	##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##'''
	im.N2         = 100## N : Number of mess points for instantaneous reliability / availability
	im.dt         = float(im.MT)/float(im.N2)
	im.tlist      = [ ( i * im.dt ) for i in range(1,im.N2+1)]
	im.avai_array = [[0 for i in range(im.N2)] for j in range(3)]## Array for transient availability = [instantaneous, interval]
	im.reli_array = [0 for i in range(im.N2)]## Array for transient reliability

	im.N1         = 10## N : Number of mess points for MTTF
	im.dt1        = float(im.MT)/float(im.N1)
	im.tlist1     = [ ( i * im.dt1 ) for i in range(1,im.N1+1)]
	im.MTTF       = [ 0 for i in range(im.N1)]
	im.mttfct     = [ 0 for i in range(im.N1)]
	return

def instant_availability( tt, tr, weight2=1 ):
	for i in range( len( im.tlist ) ):
		if im.tlist[ i ] <= ( tt ):
			pass
		elif im.tlist[i] > tt:
			if im.tlist[ i ] <= ( tt + tr ):
				im.avai_array[ 0 ][ i ] += weight2
				im.avai_array[ 1 ][ i ] += float( im.tlist[ i ] - ( tt ) )*weight2
			elif im.tlist[ i ] >= ( tt + tr ):
				im.avai_array[ 1 ][ i ] += float( tr )*weight2
	return
	
def instant_reliability( tt, tf, weight2 ):
	for i in range( len( im.tlist ) ):
		if im.tlist[ i ] > ( tt + tf ):
			im.reli_array[ i ] += weight2
	return

def post_process_tally():
	
	##=============##
	im.avai_array[0] = [ im.avai_array[0][i]/float(im.N*im.MBatch) for i in range(im.N2) ]
	im.avai_array[1] = [0] + [ im.avai_array[1][i]/float(im.N*im.MBatch*im.tlist[i]) for i in range(1,im.N2) ]
	
	im.reli_array = [ im.reli_array[i]/float(im.N*im.MBatch) for i in range(im.N2) ]
	
	for i in range(im.N1):
		if im.mttfct[i] != 0 :
			im.MTTF[i] = im.MTTF[i]/float(im.mttfct[i])  
		else:
			im.MTTF[i] = 0
	return

def counter_function( tf, weight1):
	j = int( tf/ im.deltat_tally) + 1
	for i in range( j, len(im.rel_count), 1 ):
		im.rel_count[i] = im.rel_count[i] + weight1
	return

def mttf_dist( tt, tf ):
	for i in range( im.N1):
		if (im.tlist1[ i ] < ( tt + im.dt1 ) ) and (im.tlist1[i] >= ( tt - im.dt1 )):
			im.MTTF[i]   += tf
			im.mttfct[i] += 1.0
	return
def counttally( tt, tf, weight1):
	try:
		time_instances
	except NameError:
		im.init_counters(tt)
	if tt > ( im.time_instances[-1] + im.deltat_tally):
		for i in range( int( (tt - im.time_instances[-1]) /im.deltat_tally ) ):
			im.time_instances.append( im.time_instances[ -1 ] + im.deltat_tally )
			im.rel_count.append( im.rel_count[ -1 ] )
	else:
		pass
	counter_function( tf, weight1 )
	return
def plot_tally( M ):
	
	file_name = 'output_rel_%d_%d_%s.txt'% (im.MBatch, im.N,im.DSNstr)
	saverel  = os.path.join(im.dir_path,file_name)
	file = open(saverel, 'a')
	file.write('Time\tUnreliability\n')
	for i in range(len(im.rel_count)):
		im.rel_count[i] = float(im.rel_count[i]) / float(im.MBatch*im.N)
		file.write('%f\t%f\n'%(im.time_instances[i],im.rel_count[i]))
	file.close()
	
	pl.figure(num=1,figsize=(8, 6), dpi=80)
	pl.subplot(1, 1, 1)

	pl.plot( im.time_instances, im.rel_count, linewidth=1.0, linestyle="-", label="SCM Reliability")
    
	#pl.ylim(0.,1.002)
	pl.ylabel("Unreliability")
	pl.xlabel("Time(hr)")
	pl.legend(loc="best")
	pl.grid(which='major', axis='y', linewidth=0.75, linestyle='--', color='0.75')
	pl.grid(which='major', axis='x', linewidth=0.75, linestyle='--', color='0.75') 
	
	rel_file_name = 'figure.png'
	savepath = os.path.join(im.dir_path,rel_file_name)
	
	pl.savefig(savepath,dpi=72)
	pl.show()
	pl.close()
	return


def init_counters_regenerative():	
	'''
	##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##
			Arrays for transient estimates in Regenerative process simulation
	##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++##'''
	im.N2         = 100## N : Number of mess points for instantaneous reliability / availability
	im.dt         = 1
	im.tlist      = [ ( i * im.dt ) for i in range(1,im.N2+1)]
	im.avai_array = [[0 for i in range(im.N2)] for j in range(3)]## Array for transient availability = [instantaneous, interval]

	# im.N1         = 10## N : Number of mess points for MTTF
	# im.dt1        = float(im.MT)/float(im.N1)
	# im.tlist1     = [ ( i * im.dt1 ) for i in range(1,im.N1+1)]
	# im.MTTF       = [ 0 for i in range(im.N1)]
	# im.mttfct     = [ 0 for i in range(im.N1)]
	return

def instant_availability_regenerative( tt, tr,  telapsed, weight2=1):
	# if tt > ( im.tlist[-1] + im.dt):
		# while tt > ( im.tlist[-1] + im.dt ):
			# im.tlist.append( im.tlist[-1] + im.dt )
			# im.avai_array[0].append(0)
			# im.avai_array[1].append(0)
			# im.avai_array[2].append(0)	
	
	tt = tt - telapsed - tr	
	
	for i in range( len( im.tlist ) ):
		im.avai_array[2][i] += 1
		if im.tlist[ i ] <= ( tt ):
			pass
		elif im.tlist[i] > tt:
			if im.tlist[ i ] < ( tt + tr ):
				im.avai_array[ 0 ][ i ] += weight2
				im.avai_array[ 1 ][ i ] += float( im.tlist[ i ] - ( tt ) )*weight2
			elif im.tlist[ i ] >= ( tt + tr ):
				im.avai_array[ 1 ][ i ] += float( tr )*weight2
	return

def post_process_tally_regenerative():
	
	for i in range(len(im.avai_array[0])):
		if im.avai_array[2][i]!=0:
			im.avai_array[0][i] = im.avai_array[0][i]/float(im.avai_array[2][i])
			im.avai_array[1][i] = im.avai_array[1][i]/(float(im.avai_array[2][i]) * im.tlist[i])
	return
	
def comp_fail_tally(batch, dt):
	
	for i in range( im.lenc ):
		if int( im.state[ i ] ) != 1:
			im.comp_unavailabilityMB[ i ][ batch ] += dt
	return
def comp_unavailability_cal(batch, tt1):

	for i in range( im.lenc ):
		print( im.comps[i], im.comp_unavailabilityMB[i][batch], im.comp_failcounter[i][batch], tt1,'\n',)
		im.comp_unavailabilityMB[i][batch] = float(im.comp_unavailabilityMB[i][batch])/float(tt1)
		im.comp_failcounter[i][batch] = float(im.comp_failcounter[i][batch])/float(tt1)
	return
def cal_avg_var(list):
	l   = len(list)
	avg = float(sum(list)) / float(l)
	var = 0.0
	for i in range(l):
		var = var + ( list[ i ] - avg ) ** 2
	return [ avg, var ]