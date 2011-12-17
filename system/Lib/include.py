


FULL_STRUCTURE = 'Brain Lib Node Panel Toolbar Template ViewerProcess'.split()

MIN_STRUCTURE = 'Brain Lib Node Panel Toolbar'.split()

TOOLBAR_STRUCTURE = [ 'Animation' , 'Axis' , 'Node Graph' , 'Nodes' , 'Nuke' , 'Pane' , 'Properties' , 'Viewer' ]


def ADD_RECURSIVE( shell_or_path ):
	
	''' Given a shell or path to folder, add recursively all child folders to the nuke plugin path '''
	
	shell = Normalize.shell( shell_or_path )
	
	#print 'Recursive pluginAddPath to root folder : %s' % shell['$PATH'] 
	
	for folder in shell._['$FOLDERS']:
		
		#print folder
		
		nuke.pluginAddPath( folder )



def SHELL2MENU( shell_or_path , toolbar = 'Nuke' , memory = True ):
	
	# Shell to menu , Generate Menus
	
	shell = Normalize.shell( shell_or_path )
	
	ADD_RECURSIVE( shell )

	bpaths = shell._.__bpaths__()

	for bpath in bpaths:

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
	


# CHAIN LOADERS


def LOAD_QUEUED_TOOLSETS():

	done = []
	
	for shell, recreate , avoid in brain( 'toolsets' , [] ):

		if shell not in done:

			LOAD_TOOLSET( shell , recreate = recreate , avoid = avoid )
			
			done.append( shell )




# FAVS MANAGEMENT


def ADD_FAV( fav , path ):

	nuke.removeFavoriteDir( fav )

	nuke.addFavoriteDir( fav , path )



def ADD_FAV_ALIVE_RESOURCES():
	
	def alive_resource_search():
		
		brain.Lib.sources.normalize()
		
		brain.alive_resources_search = []
		
		for H , R , path in brain.Lib.sources.alive_resources():	
		
			#print '\n    Alive resource found %s = %s' % ( R , path )
		
			resource_label = '%s/%s' % ( H.lower() , R.upper() )
			
			resource_path = path + '/'
			
			brain.alive_resources_search.append( ( resource_label , resource_path ) )
		
		
			
			
	
	def watcher():
		
		while 1:
		
			thread = brain( 'alive_resource_search_thread' , None )
		
			if thread and not thread.is_alive():
				
				#print '\nAlive Resources found:\n'
				
				for resource_label , resource_path in brain.alive_resources_search:
					
					#print '      >> %s' % resource_label
					
					nuke.removeFavoriteDir( resource_label )
					nuke.addFavoriteDir( resource_label , resource_path )
			
				del brain.alive_resources_search
				del brain.alive_resource_search_thread
				
				return
				
				
			#time.sleep( 2 )
			
			
			
	
	import threading

	brain.alive_resource_search_thread = threading.Thread( None , alive_resource_search )
	
	brain.alive_resource_search_thread.start()
	
	threading.Thread( None , watcher ).start()




def GUI_LOAD_QUEUED_TOOLSETS():

	done = []

	for shell, recreate , avoid in brain( 'toolsets' , [] ):

		if shell not in done:
			
			GUI_LOAD_TOOLSET( shell , avoid )
			
			done.append( shell )
		

	




# INDIVIDUAL LOADERS
	
	
def LOAD_TOOLSET( shell_or_path , recreate = False , avoid = [] ):
	
	shell = Normalize.shell( shell_or_path )
	
	shell( 'Brain/Hotkeys.memory' ) # ( autocreate Hotkeys.memory file)

	if recreate:
		
		RECREATE( shell )


	FOLDERS = [ F for F in shell['$FOLDER_NAMES'] if F not in avoid ]


	if 'Toolbar' in FOLDERS:
		
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
		
		print '\n    /Panel'

		registerPanels( shell.Panel._ )
		
		SHELL2MENU(  shell.Panel , 'Nuke' )
	
	
	
	if 'ViewerProcess' in FOLDERS:   	
	
		print '\n    /ViewerProcess'
		
		registerViewerProcess( shell.ViewerProcess )
		

	
	if 'Toolbar' in FOLDERS:
		
		print '\n    /Toolbar'
		
		SHELL2MENU( shell.Toolbar , None ) # folder based
		
	
	if 'Template' in FOLDERS:
		
		TEMPLATE( shell.Template )
	
	
	for fn in [ fn for fn in shell['$FILE_NAMES *.menu'] ]:
		
		# .menu files in Toolset root
		
		name  =  shell( fn )['name']

		menu_brain = Brain() 
    	
		menu_brain( 'toolbar' , 'Nuke' )
		
		menu_brain << shell( fn )
		
		shell( fn )['write']( menu_brain['code'] , backup = False )
		
		SHELL2MENU(  shell( name ) , menu_brain.toolbar )
				
		




# REGISTER FUNCTIONS

	
def registerUserNodes( toolset_shell ):
	
	userNode_files = toolset_shell._['$FILES *.userNode'] + toolset_shell._['$FILES *.uNode']	
	
	for f in userNode_files:
		
		nbrain = brain.Lib.nodeScript2.nodeBrain( f )

		brain.nodeScript( 'byNode' , { } )[ nbrain.name ] = nbrain
	


def registerPanels(  panels_shell ):
	
	panel_files = panels_shell['$FILES *.panel']
	
	#print panel_files
	
	for path in panel_files:
			
		brain.Lib.panel3.Static_Panel( path )
		
		
		
def registerViewerProcess(  viewerProcess_shell ):


	nuke.pluginAddPath( viewerProcess_shell.__path__ )

	files = viewerProcess_shell._['$FILES']

	for path in files:

		dirname, basename = os.path.split(path)
		name, ext = os.path.splitext( basename )

		print '      VP : %s' % basename
		
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
		
		
		label = cmd_name
		
		hotkey = brain( 'Hotkeys.%s' % cmd_name , '' , create_att = False  )
		
		icon = None
	
	
	
	config = Brain() << defaultConfig
	
	def reset():
		
		# Reset command memory file
		
		config.hotkey = ''		
		config >> sh( memory_file )

	# Check if memory file is present and push into config 
	
	if memory: # argument
	
		if os.path.isfile( memory_file ):


			memory_config = Brain() << sh( memory_file )
		
			config << memory_config 
		
			#print memory_config['items'] , config['items']
		
			if not memory_config['items'] == config['items']:
			
				#print 'DEBUG 2'
			
				config >> sh( memory_file )
			
				print '\nCommand memory file updated : %s\n\n' % memory_file
			
			
		
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
			
		nuke_menu.addMenu( submenu_route_string , submenu_icon  )
		
	
	route.append( config.label )

	route_string = '/'.join( route )

	hotkey = brain( 'Hotkeys.%s' % cmd_name , config.hotkey , create_att = False  )
	
	icon = config.icon or find_icon_from_bpath( bpath + [ cmd_name ] , extend = ( 0 if toolbar else 1 ))          
	
	
	nuke_menu.addCommand( route_string , auto_command , hotkey , icon  )	 
	
	print '		addCommand DBG' ,  route_string , auto_command , hotkey , icon
	





