import matplotlib.pyplot as plt
import itertools
import __init__ as im
import time
from copy import deepcopy
import pylab as pl
import os
from output_files_write import *
def main():
	opwrite()
	im.init_counters()
	
	im.perm_init_rate = deepcopy(im.rates)
	im.perm_exec_seq  = deepcopy(im.exec_seq)
	im.perm_firsttime = deepcopy(im.firsttime)
	
	
	unreliabilityMB   = [ 0 for j in range(im.MBatch) ]
	stdVariance_rel   = [ 0 for j in range(im.MBatch) ]

	unavailabilityMB  = [ 0 for j in range(im.MBatch) ]
	stdVariance_ava   = [ 0 for j in range(im.MBatch) ]
	
	inst_unavaiMB     = [ 0 for j in range(im.MBatch) ]
	stdVaria_inst_ava = [ 0 for j in range(im.MBatch) ]

	im.comp_unavailabilityMB = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.comp_failcounter      = [ [0 for j in range( im.MBatch ) ] for i in range( im.lenc ) ]
	im.simulation_time       = [  0 for j in range( im.MBatch ) ]
	comp_stdVariance_ava     = [  0 for i in range( im.lenc   ) ]

	starttime         = time.clock()
	
	im.cutsetslist    = []
	for k in range( im.MBatch ):

		tally  = 0
		downta = 0
		downti = 0
		for j in range(im.N):
			im.initialization()
			print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b'*10, k, j, tally,end = '')

			tt       = 0.0
			weight2  = 1.0
			sysfail  = 1
			rflag    = 1
			im.firsttime = deepcopy(im.perm_firsttime)
			while tt < im.MT:

				## Sampling time to next transition
				[ ts, weight2 ] = im.sample_transition_time( tt, weight2)
				[ tr, comp ]    = im.testdtestedsys( tt, ts)
				tsdash          = min( [ ts, tr ] )
				# print im.state,
				## System state check
				sysfail         = im.syscheck()
				
				## Tallying
				if sysfail == 0 :
					im.firsttime = 0

					if rflag == 1:
						tally += weight2
						rflag  = 0
						im.instant_reliability( tt, 0, weight2 )
					downta += tsdash*weight2
					im.instant_availability( tt, tsdash, weight2 )

				tt    += tsdash

				## Sampling state
				[ ts, weight2 ] = im.sample_state_stodet( k, weight2, tr, comp, ts, tt )
				im.te  = [ ( im.te[i] + tsdash ) for i in range( im.lenc ) ]
				# print sysfail,'->',

			if sysfail == 0:
				downta  = downta - ( tt - im.MT )*weight2
				downti += weight2
		endtime = time.clock()

		unreliabilityMB[k]  =  float(tally) / float(im.N)
		unavailabilityMB[k] =  float(downta) / float(im.N*im.MT)
		inst_unavaiMB[k]    =  float(downti) / float(im.N)
 		#print(k,'Unrel=%.3e'%unreliabilityMB[k],'Unavai=%.3e'%unavailabilityMB[k],"inst unava=%.3e"%inst_unavaiMB[k])
		
		file = open( im.save_path, 'a')
		file.write('\n%.3e\t%.3e\t%.3e\t%.3e' % ( unreliabilityMB[k], unavailabilityMB[k], inst_unavaiMB[k], (endtime-starttime)/float(k+1) ))
		file.close()
	
	avgtime = (endtime - starttime) / float(im.MBatch * im.N)
	
	
	im.post_process_tally()
	op_transient_rel_ava_filewrite()
	
	linesty = ['o','v','s','*','d','<','h','>','8','H','D',',', '.','o']
	plt.plot(im.tlist,im.avai_array[0],label='MCS Instant', marker=linesty[2],markevery = 5)
	plt.plot(im.tlist,im.avai_array[1],label='MCS Interval', marker=linesty[3],markevery = 5)
	plt.xlabel('Time (yr)')
	plt.ylabel('Unavailability')
	plt.legend(loc='best')
	plt.savefig('{}UNAVAILABILITY{}_{}.png'.format(im.dir_path,im.N,im.perm_firsttime))
	plt.show()
	plt.close()
		
	
	plt.plot(im.tlist,im.reli_array,label='Reliability', marker=linesty.next(),markevery = 5)
	plt.xlabel('Time (yr)')
	plt.ylabel('Unreliability')
	plt.legend(loc='best')
	plt.savefig('%s\RELIABILITY%d_%d.png'%(im.dir_path,im.N,im.perm_firsttime))
	plt.show()
	plt.close()
	
	# unreliabilityTotal = float( sum( unreliabilityMB ) )/float( im.MBatch )
	# sample_Variance_rel = 0.0
	# for i in range(im.MBatch):
		# sample_Variance_rel += (unreliabilityMB[i] - unreliabilityTotal) ** 2
	# fractErr_rel = sample_Variance_rel ** 0.5 / unreliabilityTotal
	
	unavailabilityTotal = float(sum(unavailabilityMB)) / float(im.MBatch)
	sample_Variance_ava = 0.0
	for i in range(im.MBatch):
		sample_Variance_ava += (unavailabilityMB[i] - unavailabilityTotal) ** 2
	fractErr_ava = sample_Variance_ava ** 0.5 / unavailabilityTotal
	
	inst_unavaTotal = float(sum(inst_unavaiMB))/float(im.MBatch)
	sample_Vari_inst_ava = 0.0
	for i in range(im.MBatch):
		sample_Vari_inst_ava += (inst_unavaiMB[i] - inst_unavaTotal)**2
	fractErr_inst_ava = sample_Vari_inst_ava **0.5 / inst_unavaTotal
		
	
	# op_rel_filewrite(unreliabilityTotal, sample_Variance_rel, fractErr_rel, avgtime)
	op_ava_filewrite(unavailabilityTotal, sample_Variance_ava, fractErr_ava, avgtime)
	op_ava_filewrite(inst_unavaTotal, sample_Vari_inst_ava, fractErr_inst_ava, avgtime)
		
	# print '''
	# ----------------------------------------------------#'''
	# print '\n\nUnreliability    =', unreliabilityTotal
	# print 'Variance = ', sample_Variance_rel
	# print 'Fractional Error  =', fractErr_rel
	# print 'Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_rel)
	# print 'Average Time per history =', avgtime
	# print 'Figure of Merit =', (1.0 / float(sample_Variance_rel * avgtime))
	# print '''
	# ----------------------------------------------------#
	# '''
	print( '\n\nUnavailability    =', unavailabilityTotal)
	print( 'Variance = ', sample_Variance_ava)
	print( 'Fractional Error  =', fractErr_ava)
	print( 'Rt(N)*Fractional Error =', ((im.N ** 0.5) * fractErr_ava))
	print( 'Average Time per history =', avgtime)
	print( 'Figure of Merit =', (1.0 / float(sample_Variance_ava * avgtime)))
	print( '''
	#----------------------------------------------------#
	''')
	
	return;