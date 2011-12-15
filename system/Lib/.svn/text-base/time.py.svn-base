

def _get_lapse( tag ):
	
	if tag not in brain.time( 'lapse' , {} ):
		
		brain.time.lapse[ tag ] =  time.time() , [ ]

	return brain.time.lapse[ tag ]
	
	

def lap( tag ):
	
	lap , times = _get_lapse( tag )
	
	brain.time.lapse[ tag ] = time.time() , times



def lapse( tag ):

	lap , times = _get_lapse( tag )
		
	times.append( time.time() - lap )
		
	brain.time.lapse[ tag ] =  time.time() , times
			




def print_lapses( tag = None ):
	
	print '\nPrint Request for lapses with tag: %s\n' % tag  
	
	if tag:
		
		lap , times = _get_lapse( tag )
		
		print '    %s : %s' % ( tag , times )
		
	else:
		
		for tag , v in brain.time( 'lapse' , {} ).items():
			
			lap , times = v
			
			print '    %s : %s' % ( tag , times )
			
			
			
					