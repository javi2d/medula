
# usage :

# import sop_finder
# import sop


import os
import sys


MAX_LEVEL = 2	

DONE = []

def scan_level( path , scan_branches = True ):

	for P,D,F in os.walk( path ):
		
		if P in DONE:
			
			break
		
		D[:] = [ d for d in D if not d.startswith('.') ]
		
		print '    %s' %  P 
		
		if 'sop.py' in F:	
			
			print '\n FOUND : sop module found at %s' % P
			
			sys.path.append( P )
			
			return True
		
		DONE.append( P )
		
		if scan_branches:
		
			for d in D:
			
				branch = os.path.join( P , d )

				if branch not in DONE:
					
					print '   .%s' %  branch
					
					if scan_level( branch , scan_branches = False ):
						
						return True
					
					DONE.append( branch )
					
				
		
		break
			
try:

	import sop

except ImportError:

	print '\nFinding sop module ...\n'

	mfolder = os.path.dirname( __file__ ) or os.getcwd()

	while mfolder:
	
		if scan_level( mfolder ):
		
			break
		
	
		prev_mfolder = mfolder
	
		mfolder = os.path.dirname( mfolder )
	
		if mfolder == prev_mfolder:
		
			print '\n ERROR! : sop module cannot be found.'
			sys.exit()
	
	



		

	
	
