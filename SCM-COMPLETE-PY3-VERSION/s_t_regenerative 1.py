import __init__ as im
import time
import matplotlib.pyplot as plt
import itertools
from copy import deepcopy
import pylab as pl
import os
from output_files_write import *
def main():	
	opwrite()
	im.init_counters()
	# im.init_counters_regenerative()
	im.perm_exec_seq  = deepcopy(im.exec_seq)
	im.perm_init_rate = deepcopy(im.rates)
	im.perm_firsttime = deepcopy(im.firsttime)
	
	
	unavailabilityMB = [0 for j in range(im.MBatch)]
	stdVariance_ava  = [0 for j in range(im.MBatch)]

	starttime      = time.clock()
	
	im.cutsetslist    = []

	for k in range(im.MBatch):
		weight2   = 1
		tt    = 0
		tally = 0
		te_cycle = 0.0
		for j in range(im.N):
			print '\b\b\b\b\b\b\b\b\b\b'*10, j, tt, te_cycle,
			im.initialization()
			te_cycle  = deepcopy(tt)
			weight2   = 1.0
			sysfailm1 = 1#Indicator For going out of Regenerative State
			sysfail1  = 1#Indicator For system down
			while 1:##Regenerative Process

				weight1         = deepcopy(weight2)
				sysfail         = deepcopy(sysfail1)				
				im.compsdata    = deepcopy(im.permanent_initial_value)
				
				[ ts, weight2]  = im.sample_transition_time(tt, weight1)
				[ tr, comp ]    = im.testdtestedsys(tt, ts)
				
				## Stochastic/Deterministic Transition of the state
				[ts, weight2]   = im.sample_state_stodet( weight1, tr, comp, ts, tt)
				sysfail1        = im.syscheck()

				## Count Tally
				tt           += weight2 * ts
				if sysfail   == 0 and sysfail1 == 1:
					tally    += weight2 * ts
					# im.instant_availability( tt-ts-te_cycle, ts, weight2 )
					
					im.instant_availability_regenerative( tt, ts, te_cycle, weight2)
					# te_cycle = deepcopy(tt)
				elif sysfail == 0 and sysfail1 == 0:
					tally    += weight2 * ts
					# im.instant_availability( tt-ts-te_cycle, ts, weight2 )
					
					im.instant_availability_regenerative( tt, ts,  te_cycle, weight2)
					# te_cycle = deepcopy(tt)
				elif sysfail == 1 and sysfail1 == 1:
					pass
				elif sysfail == 1 and sysfail1 == 0:
					tempcutset = deepcopy(im.cutset)
					tempcutset.sort()
					if tempcutset not in im.cutsetslist:
						im.cutsetslist.append(tempcutset)
				## Check for Regenerative State
				if sysfailm1 == 1 and (im.state.count(1) != len(im.state)):##System goes out of the regenerative state
					sysfailm1 = 0
				elif sysfailm1 == 0 and (im.state.count(1) == len(im.state)):##Regeneration state achieved
					break
			
			print float( tally )/float( tt ),
		unavailabilityMB[ k ] = float( tally )/float( tt )

		file = open( im.save_path, 'a')
		file.write('\n%s' % ( str( unavailabilityMB[ k ] ) ) )
		file.close()
	
	im.post_process_tally_regenerative()
	op_transient_ava_filewrite_regenerative()
	
	# im.post_process_tally()
	# op_transient_rel_ava_filewrite()
	
	linesty = itertools.cycle( ['o','v','s','*','d','<','h','>','8','H','D',',', '.','o'] )
	plt.plot(im.tlist,im.avai_array[0],label='MCS Instant', marker=linesty.next(),markevery = 5)
	plt.plot(im.tlist,im.avai_array[1],label='MCS Interval', marker=linesty.next(),markevery = 5)
	plt.xlabel('Time')
	plt.ylabel('Unavailability')
	plt.legend(loc='best')
	plt.savefig('%s\UNAVAILABILITY%d_%d.png'%(im.dir_path,im.N,im.perm_firsttime))
	plt.show()
	plt.close()

	MBatch  = im.MBatch
	N       = im.N
	endtime = time.clock()
	avgtime = (endtime - starttime) / float(MBatch * N)

	unavailabilityTotal = float(sum(unavailabilityMB)) / float(MBatch)
	sample_Variance_ava = 0.0
	for i in range(MBatch):
		sample_Variance_ava = sample_Variance_ava + (unavailabilityMB[i] - unavailabilityTotal) ** 2

	fractErr_ava = sample_Variance_ava ** 0.5 / unavailabilityTotal
	
	op_ava_filewrite(unavailabilityTotal, sample_Variance_ava, fractErr_ava, avgtime)
	
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
	
	print '''
	#----------------------------------------------------#
	'''
	print '\n\nUnavailability    =', unavailabilityTotal
	print 'Variance = ', sample_Variance_ava
	print 'Fractional Error  =', fractErr_ava
	print 'Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_ava)
	print 'Average Time per history =', avgtime
	print 'Figure of Merit =', (1.0 / float(sample_Variance_ava * avgtime))
	print '''
	#----------------------------------------------------#
	'''