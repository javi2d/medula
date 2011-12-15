





def addCallbacks( cb_space ):
	
	if not cb_space['file']:
		
		raise RuntimeError , 'monofile space needed'
	
	
	cb_space['exec']
		
	for k,v in cb_space['user_logic'].items():
		
		cb_id = Normalize.join( cb_space['file'] , k )
		
		cb_name = k[0].upper() + k[1:]
		
		cb_add_function = getattr( nuke ,  'add' + cb_name  , None )

		if cb_add_function:

			active_callback = brain.Callbacks( cb_id , None )
		
			if active_callback:
				
				cb_remove_function = getattr( nuke ,  'remove' + cb_name  , None )
				
				cb_remove_function( active_callback )	
				
				brain.Callbacks( cb_id , None , replace_att = True )
				
				print 'DEBUG GLOBAL CALLBACK xx %s' % ( k )
				
				
			cb_add_function( v )

			brain.Callbacks( cb_id , v , replace_att = True )
			
			print 'DEBUG GLOBAL CALLBACK ++ %s >> %s' % ( k , cb_space['file'] )
			
		else:
			
			print 'DEBUG GLOBAL CALLBACK , WARNING : %s not match any nuke callback type' % k
		

