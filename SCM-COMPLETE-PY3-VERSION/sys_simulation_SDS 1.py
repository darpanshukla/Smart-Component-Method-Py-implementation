import __init__ as im
import random
def exec_laws():
	
	for i in im.exec_seq:
		l = int(im.fetchdata(i,'Law'))
		if  l == 1:
			thermo_rule(i)
		elif l == 2:
			comparator_rule(i)
		elif l == 3:
			v2by3voting_rule(i)
		elif l == 4:
			orgate_rule(i)
		elif l == 5:
			em_rule(i)
		elif l == 6:
			cr_rule(i)
		elif l == 7:
			power_supply_rule(i)
		elif l == 8:
			analog_signal_processor_rule(i)
		elif l == 9:
			manual_test(i)
		elif l == 10:
			dnd_rule(i)
		elif l == 11:
			comparator_dnd_rule(i)
		elif l == 12:
			slfit_rule(i)
		elif l == 13:
			scram_switch_rule(i)
		elif l == 14:
			pbyq_compute(i)
		elif l == 15:
			and_gate_ns_rule(i)
		elif l == 16:
			slfit_rps_rule(i)
		elif l == 17:
			or_gate_rule(i)
		elif l == 18:
			comparator_rule2(i)
		elif l == 19:
			DIAGNOSTIC_Tester(i)
		elif l == 20:
			PCSL_rule_logic(i)
	return
def syscheck():
	exec_laws()
	## SYSCHECK for AS1 of SDS1
	csr = [int(im.fetchdata('CSR_%d'%(i+1),'Position')) for i in range(9)]	
	if csr.count(0)>2:
		return 0;
	else:
		return 1;
def syscheck1():
	exec_laws()
	## SYSCHECK for AS1 of SDS1
	csr = [int(im.fetchdata('CSR_%d'%(i+1),'Position')) for i in range(9)]	
	if csr.count(0)>=2:
		return 0;
	else:
		return 1;
def syscheck2():
	exec_laws()
	## SYSCHECK for AS of SDS2
	dsr = [int(im.fetchdata('DSR_%d'%(i+1),'Position')) for i in range(3)]	
	if dsr.count(0)>=2:
		return 0;
	else:
		return 1;
def syscheck3():
	exec_laws()
	##SYSCHECK for RPS1 of SDS1
	if int(im.fetchdata('SLFIT_RPS_1','CompOutput')) == 1:
		return 1;##system sucess
	else:
		return 0;##function failure - unavailable
def syscheck4():
	exec_laws()
	## SYSCHECK for RPS2 of SDS2
	s = int(im.fetchdata('PCSL_CSAM_RPS2_SDS2','CompOutput'))
	if s==1:
		return 1
	else:
		return 0
def syscheck_SDS2_RPS():
	exec_laws()
	## SYSCHECK for RPS2 of SDS2
	s = int(im.fetchdata('PCSL_CSAM_RPS2_SDS2','CompOutput'))
	if s==1:
		return 1
	else:
		return 0
def syscheck_SDS2_RPS_Ch1():
	exec_laws()
	## SYSCHECK for Channe1 1 of RPS2 of SDS2
	s = int(im.fetchdata('Comparator_TC_CSAM1','Control Signal'))
	if s==1:
		return 1
	else:
		return 0
def syscheck5():
	exec_laws()
	## SYSCHECK for Full SDS
	csr = [int(im.fetchdata('CSR_%d'%(i+1),'Position')) for i in range(9)]	
	dsr = [int(im.fetchdata('DSR_%d'%(i+1),'Position')) for i in range(3)]
	if csr.count(0)>2 and dsr.count(0)>1:
		return 0;
	else:
		return 1;
def and_gate_ns_rule(table):
	cs1 = int(im.fetchdata(table,'CompInput1'))
	cs2 = int(im.fetchdata(table,'CompInput2'))
	
	if (int(cs1) == 1 and int(cs2) == 1) and im.state[im.comps.index(table)] == 1:
		im.dropdata(table,1,'CompOutput')##CR DOWN
	else:
		im.dropdata(table,0,'CompOutput')##CR UP
	im.scan_connection()
	return;
def analog_signal_processor_rule(table):
	signal = int(im.fetchdata(table,'Signal'))
	if im.state[im.comps.index(table)] == 1:
		im.dropdata(table,signal,'Electrical_signal')
	im.scan_connection()
	return signal;
def comparator_rule(table):
	#ref      = float(im.fetchdata(table,'ref'))
	measured = int(im.fetchdata(table,'measured'))
	cs = 0##initial position
	if (measured == 1) and im.state[im.comps.index(table)] == 1 and im.state[im.comps.index('Manual_Test')]==1:
		cs = 1;##Control Rod Drop
	im.dropdata(table,cs,'Control Signal');
	im.scan_connection()
	return;
def comparator_rule2(table):
	measured = int(im.fetchdata(table,'measured'))
	cs = 0##initial position
	if (measured == 1) and im.state[im.comps.index(table)] == 1 and im.state[im.comps.index('Manual_Test2')]==1:
		cs = 1;##Control Rod Drop
	im.dropdata(table,cs,'Control Signal');
	im.scan_connection()
	return;
def comparator_dnd_rule(table):
    Fluxref      = float(im.fetchdata(table,'Fluxref'))
    Fluxmeasured = float(im.fetchdata(table,'Fluxmeasured'))

    cs = 0##initial position
    if (int(Fluxmeasured) >= int(Fluxref)) and im.state[im.comps.index(table)] == 1:
        cs = 1;##Control Rod Drop Signal
    im.dropdata(table,cs,'Control Signal');
    im.scan_connection()
    return;
def cr_rule(table):
    SW1 = int(im.fetchdata(table,'SW_1'))
    SW2 = int(im.fetchdata(table,'SW_2'))
    position=0##initial position
    if im.state[im.comps.index(table)] == 1:
        if int(SW1)==1 or int(SW2)==1:
            position = 1##CR Down
    im.dropdata(table,position,'Position');
    im.scan_connection()
    return;
def check_channel(tablelist):
	temp = 0
	for i in tablelist:
		if im.state[im.comps.index(i)] == 1:
			temp += 1
		else:
			pass
	if temp == len(tablelist):
		return 1
	else:
		return 0
def DIAGNOSTIC_Tester(table):
	s1 = check_channel(['ASP_TC_CSAM1','Comparator_TC_CSAM1'])
	s2 = check_channel(['ASP_TC_CSAM2','Comparator_TC_CSAM2'])
	s3 = check_channel(['ASP_TC_CSAM3','Comparator_TC_CSAM3'])
	s  = [ s1, s2, s3 ]
	
	pf = float(im.fetchdata(table,'prob-of-failure'))
	
	if random.random() > pf:
		if s.count(1) == 2:
			if s1 != 1:
				im.dropdata(table,10,'LogicControl')
			elif s2 != 1:
				im.dropdata(table,11,'LogicControl')
			elif s3 != 1:
				im.dropdata( table, 12, 'LogicControl' )
		elif s.count(1) == 1 or s.count(1) == 0:
			im.dropdata( table, 2, 'LogicControl' )
		else:
			im.dropdata( table, 1, 'LogicControl' )
	else:
		pass#im.dropdata( table, 1, 'LogicControl' )
	im.scan_connection()
	return
def dnd_rule(table):
	influx   = float(im.fetchdata(table,'Flux'))
	if im.state[im.comps.index(table)] == 1:
		im.dropdata(table,influx,'Electrical_signal')
	im.scan_connection()
	return
def em_rule(table):
	current = int(im.fetchdata(table,'Current'))
	PS  = int(im.fetchdata(table,'Power Supply'))
	
	if im.state[im.comps.index(table)] == 1 and PS == 1:
		im.dropdata(table,current,'Electrical_signal')
	else:
		im.dropdata(table,0,'Electrical_signal')
	im.scan_connection()
	return;
def manual_test(table):
	# current = int(im.fetchdata(table,'CompInput1'))
	# if im.state[im.comps.index(table)] == 1 and current == 1:
		# im.dropdata(table,1,'LogicControl')
	# else:
		# im.dropdata(table,0,'LogicControl')
	return;
def or_gate_rule(table):
	cs1 = int(im.fetchdata(table,'CompInput1'))
	cs2 = int(im.fetchdata(table,'CompInput2'))
	
	if (int(cs1) == 1 or int(cs2) == 1) and im.state[im.comps.index(table)] != 0:
		im.dropdata(table,1,'CompOutput')
	else:
		im.dropdata(table,0,'CompOutput')
	im.scan_connection()
	return;
def pbyq_compute(table):
	power = int(im.fetchdata(table,'Flux'))
	flow = int(im.fetchdata(table,'Flow'))
	if im.state[im.comps.index(table)] != 0 and power == 1 and flow == 1:
		im.dropdata(table, 1, 'Electrical_signal')
	else:
		im.dropdata(table, 0, 'Electrical_signal')
		
	im.scan_connection()
	return;
	
def PCSL_rule_logic(table):
	logic = int(im.fetchdata(table,'Logic'))
	# print logic
	if im.state[im.comps.index(table)] != 0:
		if logic == int(1):
			v2by3voting_rule(table)
		elif logic == int(2):
			im.dropdata(table,1,'CompOutput')
		else:
			v1by2voting_rule(table,logic)
	return;
def power_supply_rule(table):
	return;
def scram_switch_rule(table):
	current = int(im.fetchdata(table,'CompInput'))
	force = 0
	if im.state[im.comps.index(table)] == 1:
		if int(current) == 1:
			force = 1;##CR down
	im.dropdata(table,force,'CompOutput')
	im.scan_connection()
	return;
def slfit_rps_rule(table):
	cs1a = int(im.fetchdata(table,'CompInput1A'))
	cs1b = int(im.fetchdata(table,'CompInput1B'))
	cs2a = int(im.fetchdata(table,'CompInput2A'))
	cs2b = int(im.fetchdata(table,'CompInput2B'))
	cs3a = int(im.fetchdata(table,'CompInput3A'))
	cs3b = int(im.fetchdata(table,'CompInput3B'))
	## Inverse Logic to output
	scram_signal = 0
	if int( cs1a + cs1b + cs2a + cs2b + cs3a + cs3b)>=3 and im.state[im.comps.index(table)] == 1:
		scram_signal = 1
	im.dropdata(table,scram_signal,'CompOutput')
	im.scan_connection()
	return;
def thermo_rule(table):
    #thresold = float(im.fetchdata(table,'Thresold_Temp'))
    intemp   = float(im.fetchdata(table,'Temp'))
    
    if im.state[im.comps.index(table)] == 1:
        im.dropdata(table,intemp,'Electrical_signal')
    im.scan_connection()
    return;
def v2by3voting_rule(table):
	cs1 = int(im.fetchdata(table,'CompInput1'))
	cs2 = int(im.fetchdata(table,'CompInput2'))
	cs3 = int(im.fetchdata(table,'CompInput3'))
	## Inverse Logic to output
	current = 0
	if int( cs1 + cs2 + cs3)>=2 and im.state[im.comps.index(table)] == 1:
		current = 1
	im.dropdata(table,current,'CompOutput')
	im.scan_connection()
	return;
def v1by2voting_rule(table,l):
	
	cs1 = int(im.fetchdata(table,'CompInput1'))
	cs2 = int(im.fetchdata(table,'CompInput2'))
	cs3 = int(im.fetchdata(table,'CompInput3'))
	
	if l == 10:
		cs = cs2 + cs3
	elif l == 11:
		cs = cs1 + cs3
	elif l == 12:
		cs = cs1 + cs2
	current = 0
	if int( cs )>=1 and im.state[im.comps.index(table)] == 1:
		current = 1
	im.dropdata(table,current,'CompOutput')
	im.scan_connection()
	return;
