

def initialize_in_debug_mode():
	
	print '\nSTARTING NUKE IN DEBUG MODE'
	
	cwd( 'medula.py' )['rewrite']( '' )
	

def initialize_in_worker_mode():
	
	if not nuke.GUI:
			
		avoid = [ 'Node' ]
       
		brain.Lib.include.TOOLSET( medula.knife , avoid = avoid )
       
		brain.Lib.include.TOOLSET( local.home , avoid = avoid )
       
		brain.Lib.include.TOOLSET( local._user , avoid = avoid )
	
		worker_code = '''\nbrain.KEEP_KNOBS = True\nmedula.knife.Lib.worker.py().start()'''
	
		cwd( 'medula.py' )['rewrite']( worker_code )
		
		
	else:
		
		raw_input( '\n\nWORKER SYNTAX IS :  nuke -t medula_worker.py , press a key to exit ' )
		
		sys.exit()



def initialize_in_regular_mode():

	# This is the regular startup
	
	# Add Fav paths
	
	brain.Lib.include.ADD_FAV( '[ local ]' , local['$PATH'] )
	
	brain.Lib.include.ADD_FAV( '[ current_unit ]' , this.UNIT_PATH + '/' )
	
	#brain.Lib.include.ADD_FAV_ALIVE_RESOURCES()


	# Include Toolsets
	
	brain.Lib.include.TOOLSET( medula.knife )
	
	if not use_per_user_toolset and not use_per_project_toolset:
					
		brain.Lib.include.TOOLSET( local.home , recreate = True )
		
	else:
		
	
		brain.Lib.include.TOOLSET( local.home )
		
		brain.Lib.include.TOOLSET( local._user )	
		
		if this.HOSTNAME in [ ]: 
			
			# Include the Development toolset to test stuff, only for TDs
		
			local._dev = local( 'development/dev' )
		
			brain.Lib.include.TOOLSET( local._dev )

			# Recreate toolset structures if needed
        
			dev_structure = [
			'Node',
			'Toolbar/Nodes/Development',
			'Toolbar/Nuke/Experimental',	
			]
		
			[ local._dev( struct ) for struct in  dev_structure ]
		

		
		
		
		#brain.AUTO_REFRESH_NODE = True
	
	


		




