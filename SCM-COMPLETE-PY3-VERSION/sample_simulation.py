#!/usr/bin/python
import __init__ as im
import math
import random
from copy import deepcopy
from scipy.optimize import bisect
def analog_rate( tt,i ):

	if ((  im.Rel_Model[i] in [5,6] ) and im.state[i]==2):
		g = im.rates[0][i]

	elif ( im.Rel_Model[i] in [3,5,6] and im.state[i]==1 ):
		g = im.rates[1][i]

	elif ( im.Rel_Model[i] == 3 and im.state[i]==0 ):
		g = im.rates[0][i]
	
	elif ( im.Rel_Model[i] == 2 and im.state[i]==0 ):
		g = im.rates[0][i]
	
	elif im.Rel_Model[i] in [ 4, 45, 46, 83 ]:
		
		if im.state[ i ] == 1:
			temp = 0
			for j in range( len( im.rates[1][i] ) ) :
				temp += weibullrate( tt, im.rates[1][i][j][0], im.rates[1][i][j][1] )
			g = temp
		elif im.state[ i ] == 0:
			g = im.rates[0][i]
	return g

def analogue_state_pdf( tt, icomp ):
	[ g, L ] = gammaL( tt )
	pnum     = analog_rate(tt, icomp )
	uf       = pnum / g
	return uf

def analogue_time_pdf( tdash, tt ):
	[ g, L ] = gammaL( tdash )
	uf       = ( 1.0 - f7( tdash, 0, tt ) ) * g
	return uf
def analogue_time_pdf_82( tdash, tt ):
	[ g, L ] = gammaL( tdash )
	uf       = ( 1.0 - f7( tdash, 0, tt ) ) * g
	return uf
	
def elapsedtimeCalc(i,tdash):
	elt = tdash
	if im.Rel_Model[i] in [45,47]:
		elt = tdash - ( int(tdash/im.TestingInterval[i]) * im.TestingInterval[i] )	
	return elt

def f8( t, rn, tdash ):
	temp1 = 0
	for i in range( im.lenc ):

		if im.Rel_Model[ i ] in [4,83]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( tdash**al - t**al )
			elif im.state[i] == 0:
				temp1 += im.rates[0][i] * ( tdash - t )
		
		elif im.Rel_Model[ i ] in [45]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				temp1 += im.rates[0][i] * ( im.te[i] - t )
				
		elif im.Rel_Model[ i ] in [46]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				pass
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( tdash - t )
				
		elif im.Rel_Model[ i ] in [47]:
			if im.state[i] == 1:
				#elapsedtime = elapsedtimeCalc(i,tdash)
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				pass
				# temp1 += im.TestRate[i] * ( im.te[i]  - t )
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( im.te[i] - t )
				
		elif im.Rel_Model[ i ] in [ 3 ]:
			temp1 += im.rates[im.state[i]][i] * ( tdash - t )
			
		elif im.Rel_Model[ i ] in [ 5, 6 ]:
			if im.state[i] == 1:
				temp1 += im.rates[1][i] * ( tdash - t )
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( tdash - t )
			elif im.state[i] == 0:
				pass
	
	try:
		f = 1.0 - math.exp( temp1 ) - rn
	except:
		print( '\n range err',t,min(im.te),tdash,im.state,im.Rel_Model,temp1)
		#print 1.0 - math.exp( temp1 ) - rn
	
	return f
def f7( t, rn, tdash ):
	temp1 = 0
	for i in range( im.lenc ):

		if im.Rel_Model[ i ] in [4,83]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				temp1 += im.rates[0][i] * ( im.te[i] - t )
		
		elif im.Rel_Model[ i ] in [45]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				temp1 += im.rates[0][i] * ( im.te[i] - t )
				
		elif im.Rel_Model[ i ] in [46]:
			if im.state[i] == 1:
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				pass
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( tdash - t )
				
		elif im.Rel_Model[ i ] in [47]:
			if im.state[i] == 1:
				#elapsedtime = elapsedtimeCalc(i,tdash)
				for j in range( len(im.rates[1][i]) ):
					l      = im.rates[1][i][j][0]
					al     = im.rates[1][i][j][1]
					temp1  += l * ( im.te[i]**al - t**al )
			elif im.state[i] == 0:
				pass
				# temp1 += im.TestRate[i] * ( im.te[i]  - t )
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( im.te[i] - t )
				
		elif im.Rel_Model[ i ] in [ 3 ]:
			temp1 += im.rates[im.state[i]][i] * ( tdash - t )
			
		elif im.Rel_Model[ i ] in [ 5, 6 ]:
			if im.state[i] == 1:
				temp1 += im.rates[1][i] * ( tdash - t )
			elif im.state[i] == 2:
				temp1 += im.rates[0][i] * ( tdash - t )
			elif im.state[i] == 0:
				pass
	
	try:
		f = 1.0 - math.exp( temp1 ) - rn
	except:
		print( '\n range err',t,min(im.te),tdash,im.state,im.Rel_Model,temp1)
		#print 1.0 - math.exp( temp1 ) - rn
	
	return f

def fail( g1, l1, zita1, batch, tt = 0 ):
	"""
	Fails One components from all component if all conditions met
	"""
	if im.firsttime in [ 1, 2 ]:
		gzita1 = float( l1 * zita1 ) / float( im.x[ 0 ] )
	elif im.firsttime in [ 0, 3, 31, 5, 7, 81, 9, 82 ]:
		gzita1 = g1 * zita1
	
	a = 0.0
	b = 0.0
	for i in range(im.lenc):
		if ( int(im.state[i]) == 1 and ( im.Rel_Model[i] in [3,5,6,7,4,45,46,47,48,83] ) ):

			b += failureratecomp(i,tt)
			
			if float(gzita1) >= a and float(gzita1) < b:
				if int(im.fetchdata(im.comps[i],'CCF'))==1:
					if random.random()<(float(im.fetchdata(im.comps[i],'Beta'))/100.0):#Common Cause failure
						ccf_id = int(im.fetchdata(im.comps[i],'CCF_ID'))
						im.ccf_counter[ccf_id] += 1
						for j in range(len(im.comps)):
							if ccf_id in im.ccf_id[j]:
								if im.state[j] == 1:
									im.state[j] = 0
									im.comp_failcounter[j][batch] += 1
									if j not in im.cutset:
										im.cutset.append(j)
					else:
						im.state[i] = 0
						im.comp_failcounter[i][batch] += 1
						if i not in im.cutset:
							im.cutset.append(i)
					break;
				elif int(im.fetchdata(im.comps[i],'CCF')) == 2:
					zitatemp = random.random()
					beta1    = float(im.fetchdata(im.comps[i],'Beta1'))/100.0
					beta2    = float(im.fetchdata(im.comps[i],'Beta2'))/100.0
					if zitatemp<beta1:#Common Cause failure
						ccf_id =  int(im.fetchdata(im.comps[i],'CCF_ID1'))
						im.ccf_counter[ccf_id]+=1
						for j in range(len(im.comps)):
							if ccf_id in im.ccf_id[j]:
								if im.state[j] == 1:
									im.state[j] = 0
									im.comp_failcounter[j][batch] += 1
									if j not in im.cutset:
										im.cutset.append(j)
						print( im.cutset)
					elif (zitatemp > beta1) and zitatemp < (beta1+beta2):	
						ccf_id =  int(im.fetchdata(im.comps[i],'CCF_ID2'))
						im.ccf_counter[ccf_id]+=1
						for j in range(len(im.comps)):
							if ccf_id in im.ccf_id[j]:
								if im.state[j] == 1:
									im.state[j] = 0
									im.comp_failcounter[j][batch] += 1
									if j not in im.cutset:
										im.cutset.append(j)
						print( im.cutset)
					else:
						im.state[i] = 0
						im.comp_failcounter[i][batch] += 1
						if i not in im.cutset:
							im.cutset.append(i)
					break;
				else:
					im.state[i] = 0
					im.comp_failcounter[i][batch] += 1
					if i not in im.cutset:
						im.cutset.append(i)
					break;
			else:
				a = deepcopy(b)
	return ;

def failureratecomp( i, tt ):
	if im.Rel_Model[i] in [5,6,2,3]:
		return im.rates[1][i]
	elif im.Rel_Model[i] in [4,46,83]:
		ls = 0
		for j in range(len(im.rates[1][i])):
			ls +=  weibullrate(tt,im.rates[1][i][j][0],im.rates[1][i][j][1])
		return ls;
	elif im.Rel_Model[i] in [45,47]:
		ls = 0
		for j in range(len(im.rates[1][i])):
			ls +=  weibullrate(im.te[0],im.rates[1][i][j][0],im.rates[1][i][j][1])
		return ls;

def gammaL( tt = 0 ):
	'''
	CW = Continuous wear
	GAN = As good as new repair
	------------------------------------------
	Rel_Model| MP | Repair |	Description
	------------------------------------------
	3			y	 - 			Repairable model
	4			y	CW 			Revealed repair   without preventive maintenance 
	45			y	CW 			Revealed repair   with    preventive maintenance 
	46			y	GAN			Unrevealed repair without preventive maintenance 
	47			y	GAN 		Unrevealed repair with    preventive maintenance 
	5			y	 -			Manual test - perfect tester
	6			y	 - 			Automatic tester - Dependent tester imperfect tester
	'''

	g = 0
	L = 0
	for i in range(im.lenc):
		if ((  im.Rel_Model[i] in [5,6] ) and im.state[i]==2):
			g += im.rates[0][i]

		elif ( im.Rel_Model[i] in [3,5,6] and im.state[i]==1 ):
			L += im.rates[1][i]
			g += im.rates[1][i]
			
		elif ( im.Rel_Model[i] in [2,3] and im.state[i]==0 ):
			g += im.rates[0][i]
			
		elif im.Rel_Model[i] in [ 4, 83 ]:# Revealed repair   without preventive maintenance
			
			if im.state[ i ] == 1:
				temp = 0
				for j in range( len( im.rates[1][i] ) ) :
					temp += weibullrate( tt, im.rates[1][i][j][0], im.rates[1][i][j][1] )
				L += temp
				g += temp
			elif im.state[ i ] == 0:
				g += im.rates[0][i]
		
		elif im.Rel_Model[i] in [ 45 ]:# Revealed repair   with    preventive maintenance
			
			# elapsedtime = elapsedtimeCalc(i,tt)
			
			if im.state[ i ] == 1:
				temp = 0
				for j in range( len( im.rates[1][i] ) ) :
					temp += weibullrate( im.te[i], im.rates[1][i][j][0], im.rates[1][i][j][1] )
				L += temp
				g += temp
			elif im.state[ i ] == 0:
				g += im.rates[0][i]
				
		elif im.Rel_Model[i] in [ 46 ]:# Unrevealed repair without preventive maintenance 
			
			if im.state[ i ] == 1:
				temp = 0
				for j in range( len( im.rates[1][i] ) ) :
					temp += weibullrate( tt, im.rates[1][i][j][0], im.rates[1][i][j][1] )
				L += temp
				g += temp
			elif im.state[ i ] == 2:
				g += im.rates[0][i]
				
		elif im.Rel_Model[i] in [ 47 ]:# Unrevealed repair with    preventive maintenance 
			
			# elapsedtime = elapsedtimeCalc(i,tt)
			
			if im.state[ i ] == 1:
				temp = 0
				for j in range( len( im.rates[1][i] ) ) :
					temp += weibullrate( im.te[i], im.rates[1][i][j][0], im.rates[1][i][j][1] )
				L += temp
				g += temp
			elif im.state[ i ] == 2:
				g += im.rates[0][i]
	return [g, L]

def repair( g3, L3, zita3 ):
	"""
	Repairs One Component if all condition met
	"""
	if im.firsttime in [ 1, 2 ]:
		num = 0
		gzita3 = ( ( g3 - L3 ) * float( zita3 - im.x[ 0 ] ) / float( 1 - im.x[ 0 ] ) )
	elif im.firsttime in [0,3,31,5,7,81,9]:
		num = L3
		gzita3 = g3 * zita3

	a = 0.0
	b = num
	for i in range(im.lenc):
		if ( im.Rel_Model[i] in [5,6,46,47] and int(im.state[i]) == 2) or (im.Rel_Model[i] in [2,3,7,4,45,83] and int(im.state[i]) == 0):
			b += im.rates[0][i]
			
			if float(gzita3) >= a and float(gzita3) < b:
				im.state[i] = 1
				if i in im.cutset:
					im.cutset.remove(i)
				break;
			else:
				a = deepcopy(b)
	return ;

def sample_state_stodet( batch, weight11, treturn, comp, nexttrantime, tt ):
	
	if treturn < nexttrantime:
		# Deterministic Return of the component
		for i in comp:
			if im.Rel_Model[i] in [45,47]:
				im.state[i] = 1
				im.te[i] = 0
			elif im.state[i] == 0 and im.Rel_Model[i] in [5,6,46]:
				im.state[i] = 2
		return [ treturn, weight11 ]
	elif treturn >= nexttrantime:
		# Stochastic Transition
		weight11 = sample_state(weight11,tt, batch,0)
		return [ nexttrantime, weight11]

def sample_state( weight2, tt, batch, comp = 0 ):

    zita2 = random.random()# Change of the im.state may be there
    [g2, L2] = gammaL(tt)
	
    if im.firsttime in [ 1, 2 ]:#Simple Failure Biasing
        if zita2 < im.x[ 0 ]:#Failure of One Component
            fail( g2, L2, zita2,batch)
            weifact2 = float( L2 ) / float( im.x[ 0 ] * g2 )
            weight2  = weight2 * weifact2
        elif zita2  >= im.x[ 0 ]:#Repair of One Component
            repair( g2, L2, zita2)
            weifact3 = float( g2 - L2 ) / float( ( 1 - im.x[ 0 ] ) * g2)
            weight2  = weight2 * weifact3
        return weight2

    elif im.firsttime in [ 0, 3, 31, 81, 9 ]:#Zero Biasing 
        if (float( zita2 ) * float( g2 )) <= float( L2 ):#Failure of One Component
            fail( g2, L2, zita2, batch, tt )
        elif (float( zita2 ) * float( g2 )) > float( L2 ):#Repair of One Component
            repair( g2, L2, zita2 )
        return weight2

    elif im.firsttime == 4:#Group Based Biasing Technique
        if zita2 <= im.x[0]:
            L2 = failgroup( 0, zita2 )
            weifact4 = float(L2) / float(im.x[0] * g2)
            weight2  = weight2 * weifact4
        elif zita2 > im.x[0] and zita2 <= sum(im.x):
            L2 = failgroup( 1, zita2 )
            weifact4 = float(L2) / float(im.x[1] * g2)
            weight2  = weight2 * weifact4	
        else:
            repairgp(g2,L2,zita2)
            weifact3 = float(g2 - L2) / float((1 - sum(im.x)) * g2)
            weight2 = weight2 * weifact3
        return weight2	

    elif im.firsttime == 5:#Scaled Biasing Technique
        kscale = float( g2 - L2 )/float( L2 )
        g2dash = ( kscale - 1 ) * L2 + g2
        if (float(zita2) * float(g2dash)) <= kscale * L2:
            fail( g2dash, ( kscale * L2 ), zita2 )
            weifact4 = float(g2dash)  / float( kscale * g2 )
            weight2  = weight2 * weifact4
        
        elif (float(zita2) * float(g2dash)) > kscale * L2:
            repair( g2dash, ( kscale * L2 ), zita2 )
            weifact4 = float(g2dash)  / float(g2)
            weight2  = weight2 * weifact4
        return weight2

    elif im.firsttime == 6:#Balanced Biasing Technique
        for i in range(im.lenc):
            if ((im.Rel_Model[i] in [5,6]) and (im.state[i] in [2])) :
                g2 += im.TestRate[i]
                
        tdash   = - float(math.log(random.random())) / float(g2)
        for i in range(im.lenc):
            if ( (zita2 >= ( float( i ) / float( im.lenc - 1.0 )))  and (zita2<(float(i + 1)/float(im.lenc-1.0)))):
                if im.state[i] == 1:
                    failcomp(i)
                    weight2 = weight2 * (im.lenc-1) * float(im.rates[1][i]) / float(g2)		
                
                elif ((im.Rel_Model[i] in [5,6]) and (im.state[i] in [2])) or (im.Rel_Model[i]==3 and (im.state[i] in [0])):
                    repaircomp(i)
                    weight2 = weight2 * (im.lenc-1) * float(im.rates[0][i]) / float(g2)	
                
                elif ((im.Rel_Model[i] in [5,6]) and (im.state[i] in [0])) :
                    im.state[i] = 2
                    weight2 = weight2 * (im.lenc-1) * float(im.TestRate[i]) / float(g2)	
                break
        return weight2

    elif im.firsttime == 7:
        
        g2t = 0
        for i in range(im.lenc):
            if ((im.Rel_Model[i] in [5,6]) and (im.state[i] in [0])) :
                g2t += im.TestRate[i]
        
        g2 += g2t
        
        if 	g2 * zita2 <= L2:
            fail( g2, L2, zita2)
        elif g2 * zita2 > L2 and g2 * zita2 <= ( g2 - g2t ):
            repair( g2, L2, zita2)
        elif g2 * zita2 > ( g2 - g2t ):
            testmode( g2 , g2-g2t, zita2)
            
        return weight2

    elif im.firsttime == 8:# Time Dependent Transition Sampling

        im.rates = deepcopy(im.perm_init_rate)
        
        for i in range(im.lenc):
            im.rates[1][i] = 0
        
        for j in range(len(im.alpha[0])):#Over all Modes of Failure
            al1 = im.alpha[0][j]
            a = 0
            b = 0
            for i in range(im.lenc):
                if ((im.Rel_Model[i] in [7]) and (im.state[i] in [1])):
                    a1 = (1.0/((im.theta[i][j])**al1)) * al1 * (tt**(al1-1))
                    a += a1
                    im.rates[im.state[i]][i] += a1 
                elif ((im.Rel_Model[i] in [7]) and (im.state[i] in [0]) and (j == im.fmod[i])):
                    b1 = im.rates[im.state[i]][i]
                    b += b1
                    
            L2 += a
            g2 += a + b
            
        
        if (float( zita2 ) * float( g2 )) <= float( L2 ):
            fail( g2, L2, zita2, tt)
        elif (float( zita2 ) * float( g2 )) > float( L2 ):
            repair( g2, L2, zita2 )
        im.rates = deepcopy(im.perm_init_rate)
        return weight2
        
    elif im.firsttime in [82]:
        weight2 = sample_state_acc_82( tt, weight2 )
        return weight2

def sample_state_acc_82( tt, weight2 ):
	
	i     = random.randint( 0, (im.lenc - 2))
	ufnum = analogue_state_pdf( tt, i )
	ufden = 1.0/(im.lenc-1.0)
	state_transition( i )
	
	weight2 *= ufnum/ufden
	return weight2

def sample_83_time( l, al, rn, tdash ):
	return ( ( tdash**al ) - (float(math.log(1-rn)) / float(l)) )**(1.0/float(al))

def sample_time_acc_81( tt, weight2 ):
	rn       = random.random()
	tdash    = tt - ( math.log( rn )/im.accL )
	
	ufnum    = analogue_time_pdf( tdash, tt )
	ufden    = im.accL * math.exp( - im.accL * ( tdash - tt ) )
	
	weight2 *=  (ufnum / ufden)
	return [ ( tdash - tt ), weight2]

def sample_time_acc_82( tt, weight2 ):
	rn       = random.random()
	tdash    = tt + rn * ( im.MT - tt )
	
	ufnum    = analogue_time_pdf( tdash, tt )
	ufden    = 1.0 / ( im.MT - tt )
	
	weight2 *=  (ufnum / ufden)
	return [ ( tdash - tt ), weight2]

def sample_time( tdash ):
	rn   = random.random()
	temp = []
	for i in range(im.lenc):
		if im.Rel_Model[i] in [ 4, 83 ]:# No maintenance
			if im.state[i] == 1:
				for j in range(len(im.rates[1][i])):## Loop over number of modes of damage
					temp.append( sample_83_time( im.rates[1][i][j][0], im.rates[1][i][j][1], rn, tdash ) - tdash)
			elif im.state[i] == 0:
				temp.append( - ( float(math.log(1-rn))/float(im.rates[0][i]) ) )

		elif im.Rel_Model[i] in [ 45 ]:
			if im.state[i] == 1:
				#elapsedtime = elapsedtimeCalc(i, tdash)
				for j in range(len(im.rates[1][i])):## Loop over number of modes of damage
					temp.append( sample_83_time( im.rates[1][i][j][0], im.rates[1][i][j][1], rn, im.te[i] ) - im.te[i] )
			elif im.state[i] == 0:## the state achieved in model 45, 46 only	
				temp.append( - ( float(math.log(1-rn))/float(im.rates[0][i]) ) )
			
		elif im.Rel_Model[i] in [ 46 ]:
			if im.state[i] == 1:
				for j in range(len(im.rates[1][i])):## Loop over number of modes of damage
					temp.append( sample_83_time( im.rates[1][i][j][0], im.rates[1][i][j][1], rn, tdash ) - tdash )
			elif im.state[i] == 0:## the state achieved in model 45, 46 only	
				pass
			elif im.state[i] == 2:
				temp.append( - ( float(math.log(1-rn))/float(im.rates[0][i]) ) )
			
		elif im.Rel_Model[i] in [ 47 ]:
			if im.state[i] == 1:
				# elapsedtime = elapsedtimeCalc(i, tdash)
				for j in range(len(im.rates[1][i])):## Loop over number of modes of damage
					temp.append( sample_83_time( im.rates[1][i][j][0], im.rates[1][i][j][1], rn, im.te[i] ) - im.te[i] )
			elif im.state[i] == 0:## the state achieved in model 45, 46 only	
				pass
			elif im.state[i] == 2:
				temp.append( - ( float(math.log(1-rn))/float(im.rates[0][i]) ) )
		
		else:
			if im.Rel_Model[ i ] in [ 3 ]:
				if im.rates[im.state[i]][i] != 0.0:
					temp.append(-(float(math.log(1-rn))/float(im.rates[im.state[i]][i])))
					
			elif im.Rel_Model[ i ] in [ 5, 6 ]:
				if im.rates[1][i] != 0.0:
					if im.state[i] == 1:
						temp.append( - (float(math.log(1-rn))/float(im.rates[1][i]) ) )
					elif im.state[i] == 2:
						temp.append( - (float(math.log(1-rn))/float(im.rates[0][i]) ) )
					elif im.state[i] == 0:
						pass
						#temp.append( - (float(math.log(1-rn))/float(im.TestRate[i]) ) )
		
	if len(temp) != 0:
		xj = bisect( f7, min(im.te), tdash + min(temp) + 1.0, args = ( rn, tdash ) )
	else:
		xj = float("inf")
	return xj - min(im.te)

def sample_time_component_based():
	temp = []
	for i in range(im.lenc-1):
		temp.append(- float(math.log(random.random())) / float(im.rates[im.state[i]][i]))
	return min(temp)
	
def direct_sample_time(g2):
	
	if g2 != 0.0:
		tstar = - float(math.log(random.random())) / float(g2)
	else:
		tstar = float('inf')
	return tstar
	
def sample_transition_time( tt, weight2, tr = 0 ):
    [g2, L2] = gammaL()

    if (im.firsttime in [1,3]):
        if (0 not in im.state) and (2 not in im.state):
            weifact1 = 1 - math.exp(- g2 * (im.MT - tt))
            weight2 = weight2 * weifact1
            zita = random.random()
            zitafactor = 1 - (zita * weifact1)
            tstar = - float(math.log(zitafactor)) / float(g2)
        else:
            tstar = direct_sample_time(g2)
        
    elif im.firsttime in [31] and g2 != 0.0:
        tm = ( int(tt/max(im.TestingInterval)) + 1 ) * max(im.TestingInterval)
        weifact1 = 1 - math.exp(- g2 * ( tm - tt))
        weight2 = weight2 * weifact1
        zita = random.random()
        zitafactor = 1 - (zita * weifact1)
        tstar = - float(math.log(zitafactor)) / float(g2)
        

    elif (im.firsttime in [ 0, 2, 4, 5, 6, 8 ]):# and g2 != 0.0:
        # tstar = direct_sample_time(g2)
        tstar = sample_time(tt)
        # tstar = sample_time_component_based()

    elif im.firsttime in [9]:
        
        if g2 != 0:
            weifact1 = 1 - math.exp( - g2 * tr)#New functions
            weight2 = weight2 * weifact1
            zita = random.random()
            zitafactor = 1 - (zita * weifact1)
            tstar = - float(math.log(zitafactor)) / float(g2)
            im.firsttime = 0
        else:
            tstar = tr + 1
        
    elif im.firsttime in [7]:
        for i in range(im.lenc):
            if ((im.Rel_Model[i] in [5,6]) and (im.state[i] in [0])) :
                g2 += im.TestRate[i]
        tstar = - float(math.log(random.random())) / float(g2)

    elif im.firsttime in [81]:
        [tstar, weight2] = sample_time_acc_81(tt,weight2)
    elif im.firsttime in [82]:
        if im.state.count(1) == len(im.state):
            [tstar, weight2] = sample_time_acc_82(tt,weight2)
        else:
            tstar = sample_time(tt)


    # elif im.firsttime in [8]:#Time Dependent Rate Weibull Sampling

        # tstar = []
        # for j in range(len(im.alpha[0])):#Over all Modes of Failure
            # al1 = im.alpha[0][j]
            # th1 = 0
            # for i in range(im.lenc):
                # if ((im.Rel_Model[i] in [7]) and (im.state[i] in [1])):
                    # th1 += 1.0/((im.theta[i][j])**al1)
                # elif ((im.Rel_Model[i] in [7]) and (im.state[i] in [0]) and (j == im.fmod[i])):
                    # th1 += im.rates[im.state[i]][i]
            # if th1 > 0:
                # th1 = (1.0/float(th1))**(1.0/float(al1))
                # tstar.append( weibull( th1, al1, random.random(), tt ) )
        # tstar = min(tstar)# Transition at minimum ti
    elif g2 == 0.0:
        tstar = float('inf')
    return [tstar, weight2]

def state_transition( icomp ):
	
	if im.Rel_Model[icomp] in [3,7,4,45,83]:
		im.state[icomp] = 1 - im.state[icomp]
	
	elif im.Rel_Model[icomp] in [5,6, 48]:
		if im.state[icomp] == 1:
			im.state[icomp] = 0
		elif im.state[icomp] == 0:
			im.state[icomp] = 2
		elif im.state[icomp] == 2:
			im.state[icomp] = 1
	return

def testdtestedsys( tt1, t1 ):
	tdrlist = []#Deterministic Return Time list
	compids = []
	for i1 in range( im.lenc ):
		if i1 not in compids:
			if im.Rel_Model[ i1 ] in [ 6, 48,47]:
				statefail = tester( i1 )
				if statefail == 0:
					n = int(float( tt1 )/float( im.TestingInterval[ i1 ] )) + 1
					tv1 = ( n * im.TestingInterval[ i1 ]) - tt1
					tdrlist.append([ tv1, [ i1 ] ])
			
			elif im.Rel_Model[ i1 ] in [ 5 ,45, 46 ]:
				statefail = tester( i1 )
				if statefail == 0:
					n = int(float( tt1 )/float( im.TestingInterval[ i1 ] )) + 1
					tv1 = ( n * im.TestingInterval[ i1 ] ) - tt1
					for k in range( im.lenc ):
						if im.Rel_Model[ k ] in [ 5, 6, 46, 47, 45 ]:
							if im.TestingInterval[ k ] == im.TestingInterval[ i1 ]:
								if im.state[ k ] == 0:
									compids.append( k )
					tdrlist.append([ tv1, compids ])

	if len( tdrlist ) != 0:
		tdrlist.sort()
		return tdrlist[ 0 ]
	else:
		return [ t1 + 1, [] ]

def tester( i1 ):##Tested Voting logic law
	if im.Rel_Model[ i1 ] in [ 5 , 46]:#Manual Test
		'''
		if int( im.state[ im.comps.index('Manual_Test') ] ) == 1:

		Assumption : Manual test failure due to human error is zero

		if random.random() > float(im.fetchdata('Manual_Test','Prob of Failure')):#Human error probability
		'''
		if im.state[ i1 ] == 0:
			return 0
		else:
			return 1
	elif im.Rel_Model[ i1 ] in [ 6, 48 ]:#Diagnostic Tester
		'''
		Assumption : Diagnostic Tester probability of failed test is zero given it is in working condition
		'''
		tester_tbl_name = str( im.fetchdata( im.comps[ i1 ], 'Tester'))
		
		if int( im.state[ im.comps.index( tester_tbl_name ) ] ) == 1:
			if im.state[ i1 ] == 0:
				return 0
			else:
				return 1
		return 1
		
	elif im.Rel_Model[i1] in [45,47]:
		return 0

def weibullrate( tt, l, al1 ):## Weibull rate calculation
	return ( l * float(al1) * (tt)**(al1-1.0) )
