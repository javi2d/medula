


# local can be redefined in medula/local/_init.py, must point to a r/w folder

local( 'home' )


if local['$PATH'] == medula.local['$PATH']:

	local._user = local._project =  local.home

else:

	local._user = local( 'users/%s' % this.USER_ID )
	local._project = local._user   
	# _project defaults to _user and redefined in main/_cbk.py  before script load 


# local.home and local.main are explicit.




# Initialization


# icons initialization

brain.Lib.include.ADD_RECURSIVE( medula.local.main.Icons )


# global configuration

this << medula.local.main._this.py
brain.Lib.callbacks.addCallbacks( medula.local.main._cbk.py )

# local configuration

#this << local( 'config/_this.py' )
#brain.Lib.callbacks.addCallbacks( local( 'config/_cbk.py' ) )


args = sys.argv

if 'debug' in args:
	
	# Debug Mode , only toolset "Debug" is loaded 
	
	if len( args ) == 2:
		
		script = Normalize.join( local.cwd , args[0] )
		
		dirname , basename , name, ext = Normalize.split( script )
		
		if os.path.exists( dirname ) and ext == '.nk':
			
			sh( script )
			
			local._dbg = medula.local( 'development/dbg' )
			
			brain.Lib.include.LOAD_TOOLSET(  local._dbg  )
		
		else:
			
			print 'Syntax : nuke <script> debug  ::  Invalid <script> argument >> %s' % script
			sys.exit()
		
	else:
		
		print 'Syntax : nuke <script> debug'
		sys.exit()

	
elif 'worker.py' in args:	
	
	# Worker Mode
	
	if len( args ) == 1 and not nuke.GUI:
		
		avoid = [ 'Node' ]
        
		brain.Lib.include.TOOLSET( medula.local.main , avoid = avoid )
        
		brain.Lib.include.TOOLSET( local.home , avoid = avoid )
        
		brain.Lib.include.TOOLSET( local._user , avoid = avoid )
		
		worker_code = '''\nbrain.KEEP_KNOBS = True\nmedula.local.main.Lib.worker.py().start()'''
		
		os.chdir( local( 'tmp' )['$PATH'] )
		
		cwd( 'worker.py' )['rewrite']( worker_code )
		
	else:
		
		print 'Syntax : nuke -t worker.py'
		sys.exit()
		

else:

	# Add Fav paths
	
	brain.Lib.include.ADD_FAV( 'LOCAL' , local['$PATH'] )
	
	brain.Lib.include.ADD_FAV( 'UNIT' , this.UNIT_PATH + '/' )
	
	#brain.Lib.include.ADD_FAV_ALIVE_RESOURCES()

	# Include Toolsets
	
	brain.Lib.include.TOOLSET( medula.local.main )
	
	brain.Lib.include.TOOLSET( local.home )
	
	brain.Lib.include.TOOLSET( local._user )
	
	# The Project toolset is loaded when a script is opened

		
	if this.HOSTNAME in ''.split(): 
	
	# Creates/Load a Development toolset to test stuff, only for TDs
	
	#if this.HOSTNAME in 'hostname1 hostname2'.split():   #hostnames separated by spaces 
		
		local._dev = medula.local( 'development/dev' )
		
		brain.Lib.include.TOOLSET( local._dev )

		# Recreate toolset structures if needed
        
		dev_structure = [
		'Node',
		'Toolbar/Nodes/Development',
		'Toolbar/Nuke/Experimental',	
		]
		
		[ local._dev( struct ) for struct in  dev_structure ]
		

		
		
		
		#brain.AUTO_REFRESH_NODE = True
	

		




