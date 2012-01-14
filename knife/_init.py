


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

	brain.Lib.include.ADD_FAV_ALIVE_RESOURCES()
	
	
	# Include Toolsets
	
	brain.Lib.include.TOOLSET( medula.knife )
	
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
	
	
######################################
##
## KNIFE INIT SEQUENCE
##
######################################


'''
This is the initialize sequence of the Knife toolset. 

This toolset make use of other three toolsets

local.home  >> medula/local/home
local._user >> medula/local/users/<host_user>
local._project >> medula/local/projects/<project_name>

The project toolset is loaded when you open a script and that script is bound to a project

Knife knows the project of the script by the Sources system


'''

#if not hasattr( sop , 'local' ):
#
#	local = sop.Expose.object(  medula( 'local' )  , 'local' )

local._user    = local( 'users/%s' % this.USER_ID )

# project toolset is loaded when a nuke .nk script is opened and the script 
# is bound into a project, meanwhile it will point to home toolset

local._project = local.home


if sys.argv[-2:] == [  'medula.py' , '-debug' ] : #'medula_debug.py'
	
	initialize_in_debug_mode()

else:
	
	# global configuration

	brain.Lib.include.THIS( medula.knife._this.py )
	brain.Lib.include.CALLBACKS( medula.knife._cbk.py )


	# local configuration, copy and uncomment to your local _init.py file, put AFTER the load of this file ( medula.knife._init() )

	#brain.Lib.include.THIS( local( 'config/_this.py' ) )
	#brain.Lib.include.CALLBACKS( local( 'config/_cbk.py' ) )


	if sys.argv[-2:] == [  'medula.py' , '-worker' ] : #'medula_worker.py'
	
		initialize_in_worker_mode()
	
	else:
	
	
		initialize_in_regular_mode()




