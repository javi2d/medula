


FULL_STRUCTURE = 'Brain Lib Node Panel Toolbar Template ViewerProcess'.split()

TOOLBAR_STRUCTURE = [ 'Animation' , 'Axis' , 'Node Graph' , 'Nodes' , 'Nuke' , 'Pane' , 'Properties' , 'Viewer' ]



def THIS( this_space ):
	
	this << this_space


def CALLBACKS( cb_space ):
	
	if not cb_space['file']:
		
		raise RuntimeError , 'monofile space needed'
	
	cb_space['exec']
	
	brain( 'Callbacks' , {} )
		
	for k,v in cb_space['user_logic'].items():
		
		cb_name = k[0].upper() + k[1:]
		
		cb_add_function = getattr( nuke ,  'add' + cb_name  , None )

		if cb_add_function:
			
			cb_id = cb_space['file'] + '/%s' % k      #Normalize.join( cb_space['file'] , k )
			
			active_callback = brain.Callbacks.get( cb_id , None )    #brain.Callbacks( cb_id , None )
		
			if active_callback:
				
				cb_remove_function = getattr( nuke ,  'remove' + cb_name  , None )
				
				cb_remove_function( active_callback )	
				
				#brain.Callbacks( cb_id , None , replace_att = True )
				
				del brain.Callbacks[ cb_id ]
				
				#print '\nDEBUG GLOBAL CALLBACK xx %s' % ( k )
				
				
			cb_add_function( v )

			#brain.Callbacks( cb_id , v , replace_att = True )
			
			brain.Callbacks[ cb_id ] = v
			
			#print '\nDEBUG GLOBAL CALLBACK ++ %s >> %s' % ( k , cb_space['file'] )
			
		#else:
			
		#	print '\nDEBUG GLOBAL CALLBACK , WARNING : %s not match any nuke callback type' % k




def ADD_RECURSIVE( shell_or_path ):
	
	''' Given a shell or path to folder, add recursively all child folders to the nuke plugin path '''

	shell = Normalize.shell( shell_or_path )

	for folder in [ f for f in shell._['$FOLDERS'] if  sh( f )['$FILE_NAMES' ] ]:
   		
			nuke.pluginAddPath( folder )


def SHELL2MENU( shell_or_path , toolbar = 'Nuke' , memory = True ):
	
	# Shell to menu , Generate Menus
	
	shell = Normalize.shell( shell_or_path )

	ADD_RECURSIVE( shell )

	bpaths = shell._.__bpaths__()
	
	if bpaths:
		
		print '\n    >> Registering Commands [ %s ]\n' % shell['$PATH']
	
		for bpath in bpaths:
		
			print '            > %s' % Normalize.join( *bpath[1:] )
		
			_command2menuitem( bpath ,  toolbar = toolbar , memory = True )
	


def MENU( shell_or_path , toolbar = 'Nuke' ):

	SHELL2MENU( shell_or_path , toolbar = toolbar )


	
def TEMPLATE( shell_or_path  ):
	
	shell = Normalize.shell( shell_or_path )
	
	SHELL2MENU(  shell , 'Nuke' )


	
def RECREATE( shell_or_path ):
	
	shell = Normalize.shell( shell_or_path )

	for name in FULL_STRUCTURE:

		shell( name )

	for name in TOOLBAR_STRUCTURE:

		shell.Toolbar( name )


	

def TOOLSET( shell_or_path , recreate = False , avoid = [] ):
	
	shell = Normalize.shell( shell_or_path )
	
	shell_name = shell['$NAME']
	
	brain.toolsets = [ item for item in brain( 'toolsets' , [] ) if not item[0]['$NAME'] == shell_name ] 
	# filter brain.toolsets to delete any reference to the toolset name
	
	item = shell , recreate , avoid

	brain.toolsets.append( item )
	
	return shell
	




# FAVS MANAGEMENT


def ADD_FAV( fav , path ):

	nuke.removeFavoriteDir( fav )

	nuke.addFavoriteDir( fav , path )



def ADD_FAV_ALIVE_RESOURCES():
	

	def alive_resource_search():
		
		brain.Lib.sources.normalize()
		
		alive_resources = []
		
		for H , R , path in brain.Lib.sources.alive_resources():	
		
			#print '\nDEBUG ADD_FAV_ALIVE_RESOURCES' , H , R , path
		
			resource_label = '%s/%s' % ( H.lower() , R.upper() )
			
			resource_path = path + '/'
			
			alive_resources.append( ( resource_label , resource_path ) )
			
		
		for resource_label , resource_path in alive_resources:
			
			nuke.executeInMainThreadWithResult( ADD_FAV , ( resource_label , resource_path ) )
				
			print '\n@@ Alive resource found %s = %s\n' % ( resource_label , resource_path )
			
		
	Core.thread( alive_resource_search ).start()
		


# CHAIN LOADERS


def LOAD_QUEUED_TOOLSETS():

	done = []
	
	for shell, recreate , avoid in brain( 'toolsets' , [] ):

		if shell not in done:

			LOAD_TOOLSET( shell , recreate = recreate , avoid = avoid )
			
			done.append( shell )





def GUI_LOAD_QUEUED_TOOLSETS():

	done = []

	for shell, recreate , avoid in brain( 'toolsets' , [] ):

		if shell not in done:
			
			GUI_LOAD_TOOLSET( shell , avoid )
			
			done.append( shell )
		

	




# INDIVIDUAL LOADERS
	
	
def LOAD_TOOLSET( shell_or_path , recreate = False , avoid = [] ):
	
	
	shell = Normalize.shell( shell_or_path )
	
	#print 'DEBUG RECREATE' , recreate , shell
	
	
	shell( 'Brain/Hotkeys.memory' ) # ( autocreate Hotkeys.memory file)

	if recreate:
		
		RECREATE( shell )


	FOLDERS = [ F for F in shell['$FOLDER_NAMES'] if F not in avoid ]


	if 'Toolbar' in FOLDERS:
		
		if not nuke.GUI:
		
			ADD_RECURSIVE( shell( 'Toolbar' ) )


	if 'Lib' in FOLDERS:
		
		brain.Lib << shell.Lib    #LIB( shell.Lib )
	
	
	if 'Brain' in FOLDERS:
		
		for path in shell.Brain['$FILES *.memory']:  #
			
			dirname , basename , name , ext = brain.Lib.path.brk( path )
	
			brain( name , Brain() ) << sh( path )
			
			
	if 'Node' in FOLDERS:

		for path in shell.Node['$FILES *.node']:

			node_space = sh( path )

			node_space()  # call node file , trigger nodeSolver

	
	registerUserNodes( shell )
	



# GUI RELATED FUNCTIONS ######################################################################	


def GUI_LOAD_TOOLSET( shell , avoid = [] ):
	
	
	print '\n\n>> Loading [ %s ] toolset\n' % shell['$NAME']
	
	FOLDERS = [ F for F in shell['$FOLDER_NAMES'] if F not in avoid ]
	
	toolset_name = shell['$NAME']
			
	if 'Panel' in FOLDERS:           

		registerPanels( shell.Panel._ )
		
		SHELL2MENU(  shell.Panel , 'Nuke' )
	
	
	
	if 'ViewerProcess' in FOLDERS:   	

		registerViewerProcess( shell.ViewerProcess )
		

	
	if 'Toolbar' in FOLDERS:
		
		SHELL2MENU( shell.Toolbar , None ) # folder based
		
	
	if 'Template' in FOLDERS:
		
		TEMPLATE( shell.Template )
	
	
	for fn in [ fn for fn in shell['$FILE_NAMES *.menu'] ]:
		
		# .menu files in Toolset root
		
		name  =  shell( fn )['name']

		menu_brain = Brain() 
    	
		menu_brain << shell( fn )
		
		#print 'DEBUG .menu CONTENT', menu_brain['names']
		
		print '    >> Registering Folder as Menu [ %s ]' % name

		if 'toolbar' not in menu_brain['names']:
		
			menu_brain( 'toolbar' , 'Nuke' )
			
			shell( fn )['write']( menu_brain['code'] , backup = False )
			
			print '\n [ %s.menu ] autofilled with default content' % name

		
		shell( fn )['write']( menu_brain['code'] , backup = False )
		
		SHELL2MENU(  shell( name ) , menu_brain.toolbar )
				
		




# REGISTER FUNCTIONS

	
def registerUserNodes( toolset_shell ):
	
	userNode_files = toolset_shell._['$FILES *.userNode'] + toolset_shell._['$FILES *.uNode']	
	
	for f in userNode_files:
		
		nbrain = brain.Lib.nodeScript3.nodeBrain( f )

		brain.nodeScript( 'byNode' , { } )[ nbrain.name ] = nbrain
	


def registerPanels(  panels_shell ):
	
	panel_files = panels_shell['$FILES *.panel']
	
	for path in panel_files:
		
		print '\n    >> Registering panel [ %s ]' % os.path.basename( path )
		
		brain.Lib.panel3.Static_Panel( path )
		
		
		
def registerViewerProcess(  viewerProcess_shell ):


	nuke.pluginAddPath( viewerProcess_shell.__path__ )

	files = viewerProcess_shell._['$FILES']

	for path in files:

		dirname, basename , name, ext = Normalize.split( path )

		print '    >> Registering [ %s ] as ViewerProcess' % os.path.basename( basename )
		
		nuke.ViewerProcess.register( name , createViewerProcessNode , ( path , ) )



def createViewerProcessNode( path ):

	dirname, basename = os.path.split(path)

	name, ext = os.path.splitext( basename )	

	if ext in ['.3dl','.csp','.cub','.cube','.vf','.vfz','.blut' ]:

		n = nuke.createNode( "Vectorfield" )

		n.knobs()['vfield_file'].setValue( path )

		Names = ['interpolation', 'gpuExtrapolate', 'colorspaceIn', 'colorspaceOut']

		for Value in main.brain.CONFIG( 'Luts%s' % ext , ['trilinear field' , True , 'linear' , 'linear'] ):

			name = Names.pop(0)
			n.knobs()[ name ].setValue( Value )

		return n

	elif ext in ['.gizmo']:

		n = nuke.createNode( basename )

		return n

	else:

		print 'File extension in ViewerProcess folder not matching'	
		
		



# MENU RELATED FUNCTIONS


def _resolve_digit_start_names( name ):

	if name.startswith( '_' ):

		splitted_name = name.split('_')

		if splitted_name[1].isdigit() and len(splitted_name)>2:

			name = '_'.join( splitted_name[2:] )

	name = name.replace('_' , ' ').strip()

	return name



def find_icon(  bpath , ref ):
	
	dirname , basename = os.path.split( bpath[0] )
	
	bpath = [ dirname , basename ] + bpath[1:]
	
	while bpath:
		
		shell = sh( Normalize.join( *bpath ) )
		
		potential_icon = ref + '.png'
		
		#print
		#print 'Potential Icon : ', potential_icon
		#print 'File_Names: ', shell['$FILE_NAMES']
		#print 'Search Path: ' ,  shell['$PATH']
		#print '\n'
		
		
		if potential_icon in shell['$FILE_NAMES']:
			
			#print '\nFOUND ICON %s in %s\n' % ( potential_icon ,  shell['$PATH'] )
			
			return shell( potential_icon )['file']
		
		ref = os.path.basename( bpath.pop() ) 
	


def _filter_name( name , pattern = "^_\d+_" ):

	import re 

	matches = re.findall( pattern , name, re.IGNORECASE)

	if matches:

		name = name.replace( matches[0] , '' , 1 )

	return name.replace( '_' , ' ' ).lstrip()
		


def _command2menuitem( bpath , toolbar = None , memory = True ):
	
	
	#print 'DBG1' ,  bpath , toolbar

	cmd_name = bpath.pop()
		
	shell = sh( Normalize.join( *bpath ) )

	cmd_space = getattr( shell , cmd_name )
	
	#toolbar_name = toolbar

	auto_command = "sh('%s').%s()" % ( shell['$PATH'] , cmd_name )	
		
	auto_icon = find_icon( bpath , cmd_name )

	memory_file = Normalize.join( shell['$PATH'] , cmd_name + '.memory' )
	
	
	class defaultConfig:
		
		#toolbar = toolbar_name
		#cmd = auto_command
		
		label = _filter_name( cmd_name  )
		
		hotkey = brain( 'Hotkeys.%s' % cmd_name , '' , create_att = False  )
		
		icon = None
	
	# Convert defaultConfig to a brain structure
	
	config = Brain() << defaultConfig
	
	# Check if memory file is present and push into config 
	
	if memory: # argument
	
		if os.path.isfile( memory_file ):

			
			try:
			
				memory_config = Brain() << sh( memory_file )
			
				config << memory_config 
		
				#print memory_config['items'] , config['items']
		
				if not memory_config['items'] == config['items']:
			
					#print 'DEBUG 2'
			
					config >> sh( memory_file )
			
					print '\nCommand memory file updated >> %s\n\n' % os.path.basename( memory_file )
			
			except:
				
				nuke.warning( 'Error in command memory file >> %s' % os.path.basename( memory_file ) )
				
				if Core.__interpreter__:
					
					Core.__interpreter__.showsyntaxerror()
				
				
				
		else:
			# Create a new 	memory_file	
		
			config.hotkey = ''
			config >> sh( memory_file )
	


	# toolbar is an kwarg, None by default
	
	toolbar_name = toolbar
	
	if toolbar_name: # for single folders
		
		nuke_menu = nuke.menu( toolbar_name )
		
		dirname, basename = os.path.split( bpath.pop(0) )
		
		bpath = [ dirname , basename ] + bpath
		
		route = bpath[1:] 
		
	else: # for Toolbar folder
		
		toolbar_name = bpath[1]	
		
		nuke_menu  = nuke.toolbar( toolbar_name )  #nuke.menu( toolbar_name )		
		
		route = bpath[2:] 


	todo_submenus = route[:]  
		
	if toolbar:

		todo_icons = bpath
		
	else:
		
		todo_icons = list( os.path.split( bpath[0] ) ) + bpath[1:] 
	
	
	
	done = []
		
	submenu_routes = [ ]
	
	while todo_submenus:
		
		submenu_name = todo_submenus.pop( 0 )
		
		done.append( submenu_name )
		
		submenu_route_string = '/'.join( done )
		
		submenu_routes.append( submenu_route_string )
	
	
	
	def find_icon_from_bpath( bpath , extend = 0 ):
		
		bpath = bpath[:]
		
		for i in range( extend ):
				
			dirname , basename = os.path.split( bpath[0] )
			
			bpath = [ dirname , basename ] + bpath[1:]
			
		icon = None
		
		while bpath:
			
			png =  bpath + [ bpath.pop() + '.png' ]
			png = Normalize.join( *png )   

			if os.path.isfile( png ):
				
				icon = png 
				break
		
		return icon
		
	
	for submenu_route_string in submenu_routes:
		
		submenu_icon = find_icon_from_bpath( bpath , extend = ( 0 if toolbar else 1 ) )
		
		#print '@@@@@@@' , submenu_route_string
		
		#submenu_route_string = '/'.join( [ _filter_name( i ) for i in submenu_route_string.split('/') ]  )
		
		nuke_menu.addMenu( submenu_route_string , submenu_icon  )
		
	
	route.append( config.label )
	
	route_string = '/'.join( route )

	hotkey = brain( 'Hotkeys.%s' % cmd_name , config.hotkey , create_att = False  )
	
	icon = config.icon or find_icon_from_bpath( bpath + [ cmd_name ] , extend = ( 0 if toolbar else 1 ))          
	
	
	
	
	nuke_menu.addCommand( route_string , auto_command , hotkey , icon  )	 
	
	#print '		addCommand DBG' ,  route_string , auto_command , hotkey , icon
	





