import os,time
import __init__ as im
def opwrite():
	##################################################################
	##################################################################
	## ==================  Input Section  ============================
	## ==============  Acquisition of Data ===========================
	##         Acquisition of Reliability Parameters
	###########=====================================##################
	##################################################################
	# L in per hour
	# mu in per hour
	# MTTR in seconds
	# TestingInterval in seconds
	##################################################################
	##################################################################
	im.Rel_Model       = [int(im.compsdata[i]['Rel_Model']) for i in im.comps]
	L                  = [eval(im.compsdata[im.comps[i]]['Failure Rate'])for i in range(len(im.comps))]
	mu                 = [float(im.compsdata[i]['Repair Rate']) for i in im.comps]
	im.MTTR            = [0 for i in im.comps]
	im.TestingInterval = [0 for i in im.comps]
	im.TestRate        = [0 for i in im.comps]
	im.lenc            = len(im.comps)
	##################################################################
	##################################################################
	
	im.ccf_id          = [[] for i in range(len(im.comps))]
	im.ccf_counter     = {}
	ccf_fr             = []
	for i in range(len(im.comps)):
		
		if im.DSNstr in ['SDS7','SDS7H']:
			if i>=21 and i<=27:
				im.dropdata(im.comps[i],11,'CCF_ID')
			if i>=75 and i<=77:
				im.dropdata(im.comps[i],12,'CCF_ID')
			if i>=78 and i<=80:
				im.dropdata(im.comps[i],13,'CCF_ID')
			if i in [82,83,85,86,88,89]:
				im.dropdata(im.comps[i],14,'CCF_ID')
		
		##################################################################
		##################################################################
		if im.Rel_Model[ i ] in [ 5, 6,45, 46,47 ]:
			im.MTTR[ i ]            = float(im.fetchdata(im.comps[ i ],'MTTR'))/3600.0
			im.TestingInterval[ i ] = float(im.fetchdata(im.comps[ i ],'TestTime'))/3600.0
			im.TestRate[ i ]        = 2.0 / im.TestingInterval[ i ]
			mu[ i ]                 = 1.0 / im.MTTR[ i ]
			if im.TestingInterval[i] == 4320.0 and (im.DSNstr in ["SDS3","SDS5","SDS1","SDS2","SDS3H","SDS5H","SDS1H","SDS2H"]):
				L[i] = 1.37e-8

		##################################################################
		##################################################################
		
		if im.DSNstr in ["SDS3","SDS5","SDS1","SDS2","SDS3H","SDS5H","SDS1H","SDS2H"]:
			if int(im.fetchdata(im.comps[i],'CCF')) == 2:
				im.dropdata(im.comps[i],1,'CCF')
		
		if int(im.fetchdata(im.comps[i],'CCF')) == 1:
			x = int(im.fetchdata(im.comps[i],'CCF_ID'))
			im.ccf_id[i].append(x)
			im.ccf_counter[x] = 0
		
		elif int(im.fetchdata(im.comps[i],'CCF')) == 2:
			x1 = int(im.fetchdata(im.comps[i],'CCF_ID1'))
			x2 = int(im.fetchdata(im.comps[i],'CCF_ID2'))
			im.ccf_id[i].append( x1 )
			im.ccf_id[i].append( x2 )
			im.ccf_counter[x1] = 0
			im.ccf_counter[x2] = 0

		if int(im.fetchdata(im.comps[i],'CCF')) == 1:
			if (int(im.fetchdata(im.comps[i],'CCF_ID')) not in ccf_fr):
				ccf_fr.append( int(im.fetchdata(im.comps[i],'CCF_ID')))
			else:
				im.dropdata(im.comps[i],0,'CCF')
		
		elif int(im.fetchdata(im.comps[i],'CCF')) == 2:
			ccfid1 = int(im.fetchdata(im.comps[i],'CCF_ID1'))
			ccfid2 = int(im.fetchdata(im.comps[i],'CCF_ID2'))
			
			if ccfid1 not in ccf_fr:
				ccf_fr.append( int(im.fetchdata(im.comps[i],'CCF_ID1')))
				if ccfid2 not in ccf_fr:
					ccf_fr.append( int(im.fetchdata(im.comps[i],'CCF_ID2')))
				else:
					im.dropdata(im.comps[i],1,'CCF')
			else:
				im.dropdata(im.comps[i],0,'CCF')

	im.rates = [ mu, L ]

	im.dir_path  = os.path.join('output/%s'%( im.foldername ) )
	try:
		os.makedirs(im.dir_path)
	except OSError:
		pass
	##################################################################
	##################################################################
	
	file_name = 'ip_model_%d_%s_%d_%d_%d.txt'%( im.Model, im.DSNstr, im.MBatch, im.N, im.firsttime )

	im.save_path = os.path.join( im.dir_path, file_name )
	file      = open( im.save_path, 'a')
	file.write('''\n================++++++++++++++++++++++++++================
	Simulation Results Started at....
	%s
	'''%(str(time.gmtime())))
	
	temp = ['ID','Component','Rel_Model(Law)','fail rate','repair rate','test interval','MTTR','CCF','CCF_ID','Beta']
	file.write('\n%s\t%20s\tRel.Model(Law)\tfail_rate\trepair_rate\t test_interval\t MTTR\t CCF\t CCF_ID\t Beta'%(temp[0],temp[1]))

	for i1 in range(len(im.comps)):
		file.write('\n%d\t%20s\t%5d (%2d)\t%.2e\t%.2e' % ( i1, im.comps[i1], im.Rel_Model[i1], int(im.fetchdata(im.comps[i1],"Law")), L[i1], mu[i1] ) )
		file.write('\t%.2e\t%.2e\t%d\t%s' % ( im.TestingInterval[i1], im.MTTR[i1], int(im.fetchdata(im.comps[i1],'CCF')), str(im.ccf_id[i1]) ) )
	
	file.write(''' 
	Quantification model = %d
	Mission time = %f
	Acceleration = %d (parameter=%f)'''%(im.Model, im.MT, im.firsttime, im.x[0]))
	file.close()
	
	file_name = 'op_model_%d_%s_%d_%d_%d.txt'% (im.Model,im.DSNstr,im.MBatch,im.N,im.firsttime)
	im.save_path = os.path.join(im.dir_path, file_name)
	##################################################################
	##################################################################
	del mu,L
	return;
	
def op_rel_filewrite(unreliabilityTotal, sample_Variance_rel,fractErr_rel, avgtime):
	
	file_name1 = 'opSummaryRel_%d_%s_%d_%d_%d.txt'%(im.Model,im.DSNstr,im.MBatch, im.N,im.perm_firsttime)
	im.save_path1 = os.path.join(im.dir_path, file_name1)
	file = open(im.save_path1, 'a')
	
	str1 = ['Unreliability','Histories (Batches)','Variance','Fractional Error(Unrel)','Rt(N)*Fractional Error','Figure of Merit','Average time per history']
	if sample_Variance_rel != 0:
		xtemp = (1.0 / float(sample_Variance_rel * avgtime))
	else:
		xtemp = 11111111
	file.write('''
	#----------------------------------------------------#
	%s\t=\t%.4e
	%s\t=\t%d(%d)
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	#----------------------------------------------------#
	''' %(str1[0].ljust(25),unreliabilityTotal, str1[1].ljust(25), im.N, im.MBatch, str1[2].ljust(25), sample_Variance_rel, str1[3].ljust(25), fractErr_rel, str1[4].ljust(25), ((im.N**0.5)*fractErr_rel), str1[5].ljust(25), xtemp, str1[6].ljust(25),  avgtime))
	file.close()
	return;
	
def op_ava_filewrite(unavailabilityTotal, sample_Variance_ava, fractErr_ava, avgtime):
	
	file_name1 = 'opSummaryAva_%d_%s_%d_%d_%d.txt'%(im.Model,im.DSNstr,im.MBatch, im.N,im.perm_firsttime)
	im.save_path1 = os.path.join(im.dir_path, file_name1)
	file = open(im.save_path1, 'a')
	
	str1 = ['Unavailability','Histories (Batches)','Variance','Fractional Error(Unava)','Rt(N)*Fractional Error','Figure of Merit','Average time per history']
	
	if sample_Variance_ava != 0:
		xtemp = (1.0 / float(sample_Variance_ava * avgtime))
	else:
		xtemp = 11111111
	file.write('''
	#----------------------------------------------------#
	%s\t=\t%.4e
	%s\t=\t%d (%d)
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	%s\t=\t%.4e
	#----------------------------------------------------#
	''' %(str1[0].ljust(25),unavailabilityTotal, str1[1].ljust(25), im.N, im.MBatch, str1[2].ljust(25), sample_Variance_ava, str1[3].ljust(25), fractErr_ava, str1[4].ljust(25), ((im.N ** 0.5) * fractErr_ava), str1[5].ljust(25), xtemp, str1[6].ljust(25), avgtime))
	file.close()
	return;
	
def op_transient_rel_ava_filewrite():	

	file_name1 = 'op_sss_MT_%s_%d_%d_%d_tran_ra.txt'% (im.DSNstr,im.MBatch, im.N,im.perm_firsttime)
	file_name2 = 'op_sss_MT_%s_%d_%d_%d_mttf.txt'% (im.DSNstr,im.MBatch, im.N,im.perm_firsttime)
	im.save_path1 = os.path.join(im.dir_path, file_name1)
	im.save_path2 = os.path.join(im.dir_path, file_name2)

	file = open(im.save_path1,'a')
	for i in range(im.N2):
		file.write('%.4e\t%.4e\t%.4e\t%.4e\n'%(im.tlist[i],im.avai_array[0][i],im.avai_array[1][i],im.reli_array[i]))
	file.close()
	
	file = open(im.save_path2,'a')
	for i in range(im.N1):
		file.write('%.4e\t%.4e\n'%(im.tlist1[i],im.MTTF[i]))
	file.close()
	return	
def op_transient_ava_filewrite_regenerative():	

	file_name1 = 'op_sss_MT_%s_%d_%d_%d_tran_ra.txt'% (im.DSNstr,im.MBatch, im.N,im.perm_firsttime)
	im.save_path1 = os.path.join(im.dir_path, file_name1)
	
	file = open(im.save_path1,'a')
	for i in range(len(im.avai_array[0])):
		file.write('%.4e\t%.4e\t%.4e\t%.4e\n'%(im.tlist[i],im.avai_array[0][i],im.avai_array[1][i],im.avai_array[2][i]))
	file.close()
	return
def create_string(list):
	x = '\n'
	for i in list:
		if type(i) == list:
			x = string_manipulation(i)
		else:
			x += string_manipulation(list)
			break
	return x
def string_manipulation(list):
	x = ''
	for i in list:
		if type(i) == float:
			x += '%.4e'%i + '\t '
		elif type(i) == int:
			x += '%d'%i + '\t '
		elif type(i) == str:
			x += '%20s'%i + '\t '
	return x