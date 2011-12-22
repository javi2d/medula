

def shells_init():
	

	if not hasattr( space , 'local' ): 

		space.local  = sop.Expose.object( medula( 'local' ) , 'local' )

	
	# local can be redefined in medula/local/_init.py, must point to a r/w folder

	local( 'home' )
	
	# local.home no need of _shortcut 
	
	if local['$PATH'] == medula.local['$PATH']:

		# this happens when local is not redefined

		local._user = local._project =  local.home

	else:
	
		# this happens when local is redefined
	
		local._user = local( 'users/%s' % this.USER_ID )
		local._project = local._user   
		# _project defaults to _user and redefined in main/_cbk.py  before script load 


def config_init():	

	# icons initialization

	brain.Lib.include.ADD_RECURSIVE( medula.knife.Icons )


	# global configuration

	brain.Lib.include.THIS( medula.knife._this.py )
	brain.Lib.include.CALLBACKS( medula.knife._cbk.py )


	# local configuration

	#brain.Lib.include.THIS( local( 'config/_this.py' ) )
	#brain.Lib.include.CALLBACKS( local( 'config/_cbk.py' ) )




# Open the script using 

if 'medula_debug.py' in sys.argv:

	print '\nSTARTING NUKE IN DEBUG MODE'
	
	cwd( 'medula_debug.py' )['rewrite']( '' )
		
	
elif 'medula_worker.py' in sys.argv:
	
	
	if not nuke.GUI:
		
		
		shells_init()
		config_init()
		
		
		avoid = [ 'Node' ]
       
		brain.Lib.include.TOOLSET( medula.knife , avoid = avoid )
       
		brain.Lib.include.TOOLSET( local.home , avoid = avoid )
       
		brain.Lib.include.TOOLSET( local._user , avoid = avoid )
	
		worker_code = '''\nbrain.KEEP_KNOBS = True\nmedula.knife.Lib.worker.py().start()'''
	
		os.chdir( local( 'tmp' )['$PATH'] )
	
		cwd( 'medula_worker.py' )['rewrite']( worker_code )
		
		
	else:
		
		raw_input( 'WORKER SYNTAX IS :  nuke -t medula_worker.py , press a key to exit ' )
		
		sys.exit()
		
		
else:
	
	shells_init()
	config_init()
	
	
	# This is the regular startup
	
	# Add Fav paths
	
	brain.Lib.include.ADD_FAV( '[ local ]' , local['$PATH'] )
	
	brain.Lib.include.ADD_FAV( '[ current_unit ]' , this.UNIT_PATH + '/' )
	
	#brain.Lib.include.ADD_FAV_ALIVE_RESOURCES()


	# Include Toolsets
	
	brain.Lib.include.TOOLSET( medula.knife )
	
	if local['$PATH'] == medula.local['$PATH']:
		
		# If local is not redefined, home toolset folder structure is recreated.
		
		brain.Lib.include.TOOLSET( local.home , recreate = True )
		
		# at this point, local._user and local._project points to local.home
		
	else:
		
	
		brain.Lib.include.TOOLSET( local.home )
		
		brain.Lib.include.TOOLSET( local._user )	
		
		# the toolset local._project is loaded when a script is opened, at this moment points to local._user toolset

		
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
	

		




