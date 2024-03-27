import time
from copy import deepcopy
#import pylab as pl
import os
import __init__ as im
from output_files_write import *
def main():
	opwrite()
		
	im.perm_exec_seq  = deepcopy( im.exec_seq  )
	im.perm_init_rate = deepcopy( im.rates     )
	im.perm_firsttime = deepcopy( im.firsttime )
		
	unavailabilityMB  = [ 0 for j in range( im.MBatch ) ]
	im.sysfailcounter = [ 0 for j in range( im.MBatch ) ]

	im.comp_unavailabilityMB = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.comp_failcounter      = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.simulation_time       = [  0 for j in range( im.MBatch ) ]
	comp_stdVariance_ava     = [  0 for i in range( im.lenc   ) ]

	starttime      = time.time()
	im.cutsetslist = []

	for k in range(im.MBatch):
		weight2   = 1
		tt        = 0
		tally     = 0
		for j in range(im.N):
			
			im.initialization()
			im.firsttime = deepcopy(im.perm_firsttime)
			weight2      = 1.0
			sysfailm1    = 1    #Indicator For going out of Regenerative State
			sysfail1     = 1    #Indicator For system down
			while 1:##Regenerative Process
				
				weight1         = deepcopy( weight2                    )
				sysfail         = deepcopy( sysfail1                   )
				im.compsdata    = deepcopy( im.permanent_initial_value )
				
				[ ts, weight2 ] = im.sample_transition_time( tt, weight1 )
				[ tr, comp    ] = im.testdtestedsys( tt, ts              )
				
				ctime           = min( [ ts, tr ] )
				im.comp_fail_tally( k, ctime )
				## Stochastic/Deterministic Transition of the state
				[ ts, weight2 ] = im.sample_state_stodet( k, weight1, tr, comp, ts, tt )
				sysfail1        = im.syscheck()

				## Count Tally
				tsd           = weight2 * ts
				tt           += tsd
				if sysfail   == 0 and sysfail1 == 1:
					tally    += tsd
				elif sysfail == 0 and sysfail1 == 0:
					tally    += tsd
				elif sysfail == 1 and sysfail1 == 1:
					pass
				elif sysfail == 1 and sysfail1 == 0:
					im.firsttime            = 0
					im.sysfailcounter[ k ] += 1
					tempcutset = deepcopy( im.cutset )
					tempcutset.sort()
					if tempcutset not in im.cutsetslist:
						im.cutsetslist.append( tempcutset )
				
				## Check for Regenerative State
				if sysfailm1   == 1 and ( im.state.count(1) != len( im.state ) ):##System goes out of the regenerative state
					sysfailm1 = 0
				elif sysfailm1 == 0 and ( im.state.count(1) == len( im.state ) ):##Regeneration state achieved
					break
			
			print( '\b\b\b\b\b\b\b\b\b\b'*10,  '  %.4e'%(float( tally )/float( tt )), im.sysfailcounter[k], '%.3e'%tt, j, end='')
		unavailabilityMB[ k ]   = float( tally )/float( tt )
		im.comp_unavailability_cal( k, tt )
		im.simulation_time[ k ] = tt
		im.sysfailcounter[ k ]  = float( im.sysfailcounter[ k ] )/float( tt ) 

		file = open( im.save_path, 'a')
		file.write('\n%s' % ( str( unavailabilityMB[ k ] ) ) )
		file.close()
	
	MBatch  = im.MBatch
	N       = im.N
	endtime = time.time()
	avgtime = (endtime - starttime) / float(MBatch * N)

	[unavailabilityTotal, sample_Variance_ava ] = im.cal_avg_var(unavailabilityMB)
	fractErr_ava = sample_Variance_ava ** 0.5 / unavailabilityTotal
	op_ava_filewrite(unavailabilityTotal, sample_Variance_ava, fractErr_ava, avgtime)
	
	## Writing outputs for all the components' unavailability and failure frequency 
	
	im.save_path = os.path.join(im.dir_path, 'Complete_OP_Abar_and_Fail_Freq_%s.txt'%im.DSNstr)
	file = open(im.save_path, 'a')
	
	file.write('\n#System\t %s\t Average\t Variance\t %s\t Average f\t Variance f'%( create_string( [ i for i in range( im.MBatch ) ] ), create_string( [ i for i in range( im.MBatch ) ]) ))
	
	file.write( create_string( ['Simulation Times'] + im.simulation_time) )
	
	file.write( create_string( ['System'] + unavailabilityMB + im.cal_avg_var(unavailabilityMB) + im.sysfailcounter + im.cal_avg_var(im.sysfailcounter) ))
	
	
	for i in range( im.lenc ):
		tempstring = create_string( [ im.comps[i] ] + im.comp_unavailabilityMB[ i ] + im.cal_avg_var( im.comp_unavailabilityMB[ i ] ) + im.comp_failcounter[ i ] + im.cal_avg_var( im.comp_failcounter[i] ) )
		file.write( tempstring )
	file.close()
	
	## Writing cutsets in output file for 
	im.save_path = os.path.join(im.dir_path, 'CUTSET_%s.txt'%im.DSNstr)
	file = open(im.save_path, 'a')
	op_cutset = []
	for i in range(len(im.cutsetslist)):
		temp = []
		for j in im.cutsetslist[i]:
			temp.append(im.comps[j])
		op_cutset.append(temp)
	file.write(str(op_cutset))
	file.write(str(im.ccf_counter))
	file.close()
	'''
	print '''
	#----------------------------------------------------#
	'''
	print( '\n\nUnavailability    =', unavailabilityTotal
	print 'Variance = ', sample_Variance_ava
	print 'Fractional Error  =', fractErr_ava
	print 'Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_ava)
	print 'Average Time per history =', avgtime
	print 'Figure of Merit =', (1.0 / float(sample_Variance_ava * avgtime))
	print '''
	#----------------------------------------------------#
	''''''	
	return;
