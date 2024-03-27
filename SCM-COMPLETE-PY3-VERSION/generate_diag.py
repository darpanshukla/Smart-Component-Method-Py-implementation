#!/usr/bin/python
import sys
import argparse
	
parser = argparse.ArgumentParser()
parser.add_argument("DSNstr",type=str, help='''DSN name of database (Mandatory)''')
args =  parser.parse_args()

outfile= open("%s.txt"%(args.DSNstr),'r')
line = outfile.readlines()
outfile.close()
temp = eval(line[0])


###############################################
###############################################
###############################################
###############################################
diag_file = open('%s.diag'%(args.DSNstr),'w')
## Initialize output file
inistring = "blockdiag {\n"

diag_file.write(inistring)

## Create nodes
for i in temp[0]:
	diag_file.write(i)
	diag_file.write(';\n')

	
conn_name='Connector'

## Creat Edge
for i in temp[2][conn_name]:
	print( i)
	
	diag_file.write(temp[0][i[0]])
	diag_file.write(' -> ')	
	diag_file.write(temp[0][i[2]])
	diag_file.write(';\n')
	

## End the diag file
diag_file.write('}')

diag_file.close()

print( """
Now type blockdiag inputfilename.diag
press enter
""")
