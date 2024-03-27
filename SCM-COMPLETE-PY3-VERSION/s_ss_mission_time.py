
import __init__ as im
import time
from copy import deepcopy
import pylab as pl
import os
from output_files_write import *
def main():	
	opwrite()
	
	im.perm_init_rate = deepcopy(im.rates)
	im.perm_exec_seq  = deepcopy(im.exec_seq)
	im.perm_firsttime = deepcopy(im.firsttime)
	
	unreliabilityMB   = [ 0 for j in range(im.MBatch)]
	stdVariance_rel   = [ 0 for j in range(im.MBatch)]

	unavailabilityMB  = [0 for j in range(im.MBatch)]
	stdVariance_ava   = [0 for j in range(im.MBatch)]

	im.comp_unavailabilityMB = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.comp_failcounter      = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.simulation_time       = [  0 for j in range( im.MBatch ) ]
	comp_stdVariance_ava     = [  0 for i in range( im.lenc   ) ]
	
	starttime         = time.time()

	im.perm_exec_seq  = deepcopy( im.exec_seq )
	im.cutsetslist    = []
	
	for k in range(im.MBatch):

		tally = 0
		downt = 0
		for j in range(im.N):
			im.initialization()
			im.state     = [1 for i in range(im.lenc)]
			im.exec_seq  = deepcopy(im.perm_exec_seq)
			im.compsdata = deepcopy(im.permanent_initial_value)
			im.rates     = deepcopy(im.perm_init_rate)
			
			print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b', k, j, tally,end='')
			
			tt       = 0
			weight2  = 1
			sysfail  = 1
			rflag    = 1
			while tt < im.MT:

				weight1         = deepcopy(weight2)

				[ ts, weight2 ] = im.sample_transition_time(tt, weight1)
				[ tr, comp ]    = im.testdtestedsys(tt, ts)
				tsdash          = min([ts, tr])

				if ( tt + tsdash ) > im.MT:
					tsdash = im.MT - tt
				else:
					tsdash = tsdash

				sysfail = im.syscheck()

				if sysfail == 0:
					if rflag == 1:
						tally += 1
						rflag = 0
					downt += tsdash

				tt += tsdash
				## Stochastic/Deterministic Transition of the state
				if tt < im.MT:
					[ts, weight2] = im.sample_state_stodet(k, weight2, tr, comp, ts,tt)
				else:	
					if sysfail == 0 :
						downt = downt - (tt - im.MT)
					tt = im.MT

		endtime = time.time()

		unreliabilityMB[k]  =  float(tally) / float(im.N)
		unavailabilityMB[k] =  float(downt) / float(im.N*im.MT)

		print(k,'Unreliability',unreliabilityMB[k],'Unavailability=', unavailabilityMB[k])
		
		file = open( im.save_path, 'a')
		file.write('\n%s\t%s\t%f' % ( str(unreliabilityMB[k]), str(unavailabilityMB[k]), (endtime-starttime)/float(k+1) ))
		file.close()
	
	avgtime = (endtime - starttime) / float(im.MBatch * im.N)
	
	unreliabilityTotal = float( sum( unreliabilityMB ) )/float( im.MBatch )
	sample_Variance_rel = 0.0
	for i in range(im.MBatch):
		sample_Variance_rel = sample_Variance_rel+ (unreliabilityMB[i] - unreliabilityTotal) ** 2

	fractErr_rel = sample_Variance_rel ** 0.5 / unreliabilityTotal
	
	unavailabilityTotal = float(sum(unavailabilityMB)) / float(im.MBatch)
	sample_Variance_ava = 0.0
	for i in range(im.MBatch):
		sample_Variance_ava = sample_Variance_ava + (unavailabilityMB[i] - unavailabilityTotal) ** 2

	fractErr_ava = sample_Variance_ava ** 0.5 / unavailabilityTotal
	
	op_rel_filewrite(unreliabilityTotal, sample_Variance_rel,fractErr_rel, avgtime)
	op_ava_filewrite(unavailabilityTotal, sample_Variance_ava, fractErr_ava, avgtime)
	
	print('''
	#----------------------------------------------------#''')
	print('\n\nUnreliability    =', unreliabilityTotal)
	print('Variance = ', sample_Variance_rel)
	print('Fractional Error  =', fractErr_rel)
	print('Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_rel))
	print('Average Time per history =', avgtime)
	print('Figure of Merit =', (1.0 / float(sample_Variance_rel * avgtime)))
	print('''
	#----------------------------------------------------#
	''')
	print('\n\nUnavailability    =', unavailabilityTotal)
	print('Variance = ', sample_Variance_ava)
	print('Fractional Error  =', fractErr_ava)
	print('Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_ava))
	print('Average Time per history =', avgtime)
	print('Figure of Merit =', (1.0 / float(sample_Variance_ava * avgtime)))
	print('''
	#----------------------------------------------------#
	''')
	return;