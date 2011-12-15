
# usage :

# import sop_finder
# import sop


MAX_LEVEL = 2	
DONE = []

def scan_level( path , scan_branches = True ):

	for P,D,F in os.walk( path ):
		
		if P in DONE:
			
			break
		
		D[:] = [ d for d in D if not d.startswith('.') ]
		
		print '    %s' %  P 
		
		if 'sop.py' in F:	
			
			sys.path.append( P )
			
			return P
		
		DONE.append( P )
		
		if scan_branches:
		
			for d in D:
			
				branch = os.path.join( P , d )

				if branch not in DONE:
					
					if scan_level( branch , scan_branches = False ):
						
						return branch
					
					DONE.append( branch )
					
				
		
		break




if not __name__ == '__main__':


	print '\nSOP_FINDER : Finding sop.py module file...\n'

	import os
	import sys
	import __main__ as main

	import sop_finder

	main.sop_finder = sop_finder
		
	try:
	
		import sop
		
		print '\nSOP_FINDER : sop module found in sys.path'
		
	except ImportError:

		print '\nSOP_FINDER : Searching...\n'

		mfolder = os.path.dirname( __file__ ) or os.getcwd()

		while mfolder:
			
			found = scan_level( mfolder )
				
			if found:
				
				print '\nSOP_FINDER : sop module found at %s' % found
				break
		
			prev_mfolder = mfolder
	
			mfolder = os.path.dirname( mfolder )
	
			if mfolder == prev_mfolder:
		
				print '\nSOP_FINDER : ERROR! sop module cannot be found.'
				sys.exit()
	
	



		

	
	
