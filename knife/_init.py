

'''
This is the initialize sequence of the Knife toolset. 

This toolset make use of other three toolsets

local.home  >> medula/local/home
local._user >> medula/local/users/<host_user>
local._project >> medula/local/projects/<project_name>

The project toolset is loaded when you open a script and that script is bound to a project

Knife knows the project of the script by the Sources system


'''



local._user    = local( 'users/%s' % this.USER_ID )

# project toolset is loaded when a nuke .nk script is opened and the script 
# is bound into a project, meanwhile it will point to home toolset

local._project = local.home



# preload Lib/initializers.py file

initializers = space['shell'].Lib.initializers()

if sys.argv[-2:] == [  'medula.py' , '-debug' ] : #'medula_debug.py'
	
	initializers.initialize_in_debug_mode()

else:
	
	# global configuration

	brain.Lib.include.THIS( medula.knife._this.py )
	brain.Lib.include.CALLBACKS( medula.knife._cbk.py )


	# local configuration, copy and uncomment to your local _init.py file, put AFTER the load of this file ( medula.knife._init() )

	#brain.Lib.include.THIS( local( 'config/_this.py' ) )
	#brain.Lib.include.CALLBACKS( local( 'config/_cbk.py' ) )


	if sys.argv[-2:] == [  'medula.py' , '-worker' ] : #'medula_worker.py'
	
		initializers.initialize_in_worker_mode()
	
	else:
	
	
		initializers.initialize_in_regular_mode()




