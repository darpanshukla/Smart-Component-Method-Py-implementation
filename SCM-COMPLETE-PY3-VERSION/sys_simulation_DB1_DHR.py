import __init__ as im
import random,math
def syscheck( t, dt ):

	for i in im.exec_seq:
		temp_law = int( im.fetchdata( i, 'Law' ) )
		
		if temp_law==1:
			
			if 'Fuel' in im.exec_seq:
				
				law1new( i, t, dt )# 'Law of Fuel'
			
			else:
				
				law1( i, t, dt )# 'Law of RPV'
			im.scan_connection()
			
		elif temp_law==2:# 'Law of Power Supply'
			
			law2( i )
			im.scan_connection()
			
		elif temp_law==3:# 'Law of Valve'

			if 'Fuel' in im.exec_seq:
				
				law3( i, t )
				
			else:
				
				law3old( i )
			im.scan_connection()

		elif temp_law==4:# 'Law of HX'
			
			law4( i )
			im.scan_connection()
			
		elif temp_law==5:# 'Law of Coolant'
			
			law5( i, t, dt )
			im.scan_connection()
			
		elif temp_law == 6:# 'Law of Human Action'
			
			law6( i, t, dt )
			im.scan_connection()
		
		elif temp_law == 7:# 'Law of Auto Control'
			
			law7( i, t )
			im.scan_connection( )
	

	if 'Fuel' in im.exec_seq:
		trackparameters = [ [ 'Fuel', 'Tci' ],[ 'Fuel', 'T_upper_limit' ]]
		ti  = im.fetchdata(trackparameters[0][0],trackparameters[0][1])
		tl  = im.fetchdata(trackparameters[1][0],trackparameters[1][1])
		trackparameters = [ [ 'Fuel', 'Tci' ],[ 'Fuel', 'T_low_limit' ]]
		tci  = im.fetchdata(trackparameters[0][0],trackparameters[0][1])
		tcl  = im.fetchdata(trackparameters[1][0],trackparameters[1][1])
		
		sys = 1
		if ( float( ti ) > float( tl ) ) or ( float( tci ) < float( tcl ) ):
			sys = 0
		return sys;
	else:
		trackparameters = [ [ 'RPV', 'Ti' ],[ 'RPV', 'Tl' ],['RPV','Tlower']]
		ti  = im.fetchdata(trackparameters[0][0],trackparameters[0][1])
		tl  = im.fetchdata(trackparameters[1][0],trackparameters[1][1])
		sys = 1
		if ( float( ti ) > float( tl ) ):
			sys = 0
		return sys;
		
def law1(table,t,dt):
	
	p0   = float(im.fetchdata( table, 'Initial_HS') )
	
	h    = float(im.fetchdata( 'HX1', 'h') )
	A    = float(im.fetchdata( 'HX1', 'Area'))
	
	al   = float(im.fetchdata( table, 'Alpha'))
	
	mass = float(im.fetchdata( table, 'mass'))
	cp   = float(im.fetchdata( table, 'cp'))
	
	Tatm = float(im.fetchdata( table, 'Tatm'))
	Tim1 = float(im.fetchdata( table, 'Tim1'))
	Ti   = float(im.fetchdata( table, 'Ti'))
	TAlarm = float(im.fetchdata( table, 'Talarm'))
	
	#Counting Loop available
	n1   = int(im.fetchdata(table,'HR1'))
	n2   = int(im.fetchdata(table,'HR2'))
	n    = n1 + n2
	
	im.dropdata(table,Ti,'Tim1')# May be commented as Tim1 is not used anywhere
	
	if t == 0:
		
		pt = p0
	
	else:
		
		pt = p0 * ( ( t ** ( - al ) ) - ( ( t + 1e7 )**( - al ) ) )	
	
	t1   = ( pt ) - ( n * h * A * ( Ti - Tatm ) )
	t2   = float( dt * t1 )
	t3   = ( mass * cp * Ti ) + t2
	temp = float( t3 )/float( mass * cp )
	
	im.dropdata( table, temp, 'Ti')
	
	if temp < TAlarm:
		
		im.dropdata( table, 1, 'Alarm')
	
	return;

def law1new(table,t,dt):
	
	p0       = float(im.fetchdata( table, 'Initial_HS') )
	
	hclad    = float(im.fetchdata( table, 'h' ) )
	Aclad    = float(im.fetchdata( table, 'Area' ))
	
	al       = float(im.fetchdata( table, 'Alpha' ))
	
	mf       = float(im.fetchdata( table, 'mass' ))
	cpf      = float(im.fetchdata( table, 'cp' ))
	
	Tci      = float(im.fetchdata( 'Coolant', 'Tci' ))
	Tfim1    = float(im.fetchdata( table, 'Tfim1' ))
	Tfi      = float(im.fetchdata( table, 'Tfi' ))
	Talarm   = float(im.fetchdata( table, 'Talarm' ))
	
	im.dropdata( table, Tfi, 'Tfim1' )#Used in Coolant Law
	
	if t == 0:
	
		pt = p0
	
	else:
		
		pt = p0 * ( ( t ** ( - al ) ) - ( ( t + 1e7 )**( - al ) ) )	
	
	t1   = ( pt ) - ( hclad * Aclad * ( Tfi - Tci ) )
	
	t2   = float( dt * t1 )
	
	t3   = ( mf * cpf * Tfi ) + t2
	
	temp = float( t3 )/float( mf * cpf )
	
	im.dropdata( table, temp, 'Tfi' )
	
	# if temp > Talarm:
		# im.dropdata(table, 2, 'Alarm' )
	return;

def law2(table):# For Power Supply
    
	PS = im.state[ im.comps.index( table )]

	if PS==1:
		im.dropdata( table, 1, 'Power' )

	else:
		im.dropdata( table, 0, 'Power' )
	return

def law3(table,t):# For all valve component
	
	HW   = im.state[im.comps.index( table )]
	auto = int(im.fetchdata( table, 'ControlSignal1' ))
	cs   = int(im.fetchdata( table, 'ControlSignal2' ))
	
	if HW == 1:
		if t != 0:
			im.dropdata( table, cs, 'Flow' )
		
		elif t == 0:
			if ( cs == 1 or auto == 1 ):
				im.dropdata( table, 1, 'Flow' )
			elif ( cs == 0 and auto == 0 ):
				im.dropdata( table, 0, 'Flow' )
	return

def law3old(table):# For all valve component
	
	HW   = im.state[im.comps.index( table )]
	
	if HW == 1:
		
		im.dropdata( table, 1, 'Flow')
	
	else:	
		
		im.dropdata( table, 0, 'Flow')
	return;

def law4(table):# Law for Heat Exchanger

	HW    = im.state[im.comps.index(table)]
	Inlet = int(im.fetchdata(table,'Inlet'))

	if HW == 1 and Inlet == 1:
		im.dropdata(table,1,'HR')

	else:        
		im.dropdata(table,0,'HR')
	return

def law5(table,t,dt):# Law for Coolant Temperature
	
	hclad    = float(im.fetchdata( 'Fuel', 'h' ))
	Aclad    = float(im.fetchdata( 'Fuel', 'Area' ))
	
	hcool    = float(im.fetchdata( table, 'h' ))
	Acool    = float(im.fetchdata( table, 'Area' ))
	
	mc       = float(im.fetchdata( table, 'mass' ))
	cpc      = float(im.fetchdata( table, 'cp' ))
	
	Tfim1    = float(im.fetchdata( 'Fuel', 'Tfim1' ))
	Tatm     = float(im.fetchdata( table, 'Tatm' ))
	
	Tcim1    = float(im.fetchdata( table, 'Tcim1' ))
	Tci      = float(im.fetchdata( table, 'Tci' ))
	
	TAlarm   = float(im.fetchdata( table, 'Talarm'))
	
	#Counting Loop available
	n1   = int(im.fetchdata( table, 'HR1' ))
	n2   = int(im.fetchdata( table, 'HR2' ))
	n    = n1 + n2
	
	im.dropdata( table, Tci, 'Tcim1' )# May be commented as Tim1 is not used anywhere
	
	pt   = hclad * Aclad * ( Tfim1 - Tci )

	t1   = ( pt ) - ( n * hcool * Acool * ( Tci - Tatm ) )
	
	t2   = float( dt * t1 )
	
	t3   = ( mc * cpc * Tci ) + t2
	
	temp = float( t3 )/float( mc * cpc )
	
	im.dropdata( table, temp, 'Tci' )
	
	if temp < TAlarm:
		im.dropdata( table, 1, 'Alarm' )
	return;

def law6( table, t, dt ):## Law for Human Action
	
	if t == 0:## Opening Task
		
		alarm1 = int(im.fetchdata( table, 'Alarm1' ))

		if alarm1 == 1:
			thalf   = float( im.fetchdata( table, 't_half1' ))
			trhuman = - thalf * math.log( ( random.random() ) / thalf)
			im.dropdata( table, ( t + trhuman ) ,'TimeofAction')
			im.dropdata( table, 0, 'Alarm1')
		
	else:## Closing Task
		##  Assumption: human operator is always available i.e. state = 1
		
		alarm1  = int(im.fetchdata( table, 'Alarm1' ))
		alarm2  = int(im.fetchdata( table, 'Alarm2' ))

		if alarm1 == 0:
			
			trhuman = int(im.fetchdata( table, 'TimeofAction' ) )
			if  ( t >= ( trhuman - dt ) ) and ( t <= ( trhuman + dt ) ):
				zita    = random.random()
				if zita < float(im.fetchdata( table, 'pondemand' )):
					pass
		
				else:
					im.dropdata(table,1,'ControlSignal1')
					im.dropdata(table,1,'ControlSignal2')
					im.dropdata(table,1,'Alarm1')

		if alarm2 == 1:
			
			t_set   = int(im.fetchdata( table, 't_set' ))
			if t_set == 0:
				thalf   = float( im.fetchdata( table, 't_half2' ))
				trhuman = - thalf * math.log( ( random.random() ) / thalf)
				im.dropdata( table, ( t + trhuman ) ,'TimeofAction')
				im.dropdata( table, 1, 't_set')
			
			elif t_set == 1:
				
				trhuman = int(im.fetchdata( table, 'TimeofAction' ) )
				if  ( t >= ( trhuman - ( 2 * dt))) and ( t <= ( trhuman + (2*dt))):
					zita    = random.random()
					if zita < float(im.fetchdata( table, 'pondemand' )):
						pass
			
					else:
						n1   = int( im.fetchdata( 'Coolant', 'HR1' ))
						n2   = int( im.fetchdata( 'Coolant', 'HR2' ))
						n    = n1 + n2
					
						if n == 2:
							im.dropdata( table, 0, 'ControlSignal1')
							im.dropdata( table, 0, 'ControlSignal2')
					im.dropdata( table, 0, 'Alarm2')
					im.dropdata( table, 0, 't_set')
	return;

def law7( table, t ):# Law of Auto Control
	
	if t == 0:

		pw = int( im.fetchdata( table, 'Power' ))
		
		if im.state[im.comps.index(table)] != 0 and pw == 1:
			
			zita    = random.random()
			
			if zita < float(im.fetchdata( table, 'Failure Rate' )):
				pass
			
			else:
				im.dropdata( table, 1, 'ControlSignal' )
		return;
	
	else:
		return;