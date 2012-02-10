
############################################################################################################################################
# nodeBrain and support functions


def filter_tab_value( tab_value , nbrain ):
	
	tab_path = None
	
	if type( tab_value ).__name__ in ['str','unicode']:

		tab_path = nbrain.shell( tab_value ).__file__

	elif type( tab_value ).__name__ == 'Space':

		tab_path = tab_value.__file__

	else:

		print 'WARNING!! Syntax Invalid tab value : [ %s ] ' % tab_value
	
	#print 'DEBUG09098 ' , nbrain.basename , tab_path 
	
	return tab_path




def update_nbrain( path ):
	
	# Informacion fija solo creada una vez
	
	dirname , basename = os.path.split( path )
	name , ext = os.path.splitext( basename )
	
	
	nbrain = brain.nodeScript( 'byBasename' , {} ).get( basename , None )
	
	if not nbrain:
		
		nbrain = brain.nodeScript.byBasename[ basename ] = sop.Brain()
	
		
	nbrain.path = path

	nbrain.name = name
	
	nbrain.basename = basename 
	
	nbrain.ext  = ext

	nbrain.shell = sop.sh( dirname )
	
	nbrain.space = __execute_with_knobs( path )
		
	nbrain.tabs = []
	
	if hasattr( nbrain.space , 'TABS' ):
		
		for tab_value in nbrain.space.TABS:
			
			normalized_path = filter_tab_value( tab_value , nbrain ) 
			
			if normalized_path:
			
				nbrain.tabs.append( normalized_path  )
			
	
	if nbrain.path not in nbrain.tabs:
		
		nbrain.tabs = [ nbrain.path ] + nbrain.tabs
	
	#print '\n>> updated nbrain for %s' % path
	
	return nbrain



def remove_applied_callbacks( path ):

	# get rid of old nbrain applied callbacks
	
	

	nbrain = brain.nodeScript( 'byBasename' , {} ).get( os.path.basename( path ) , None )

	if nbrain:
					
		node_class = nbrain.name # valid only for Nodes, not PanelNodes

		applied_callbacks = nbrain( 'applied_callbacks' , [] )
		
		for applied_callback in applied_callbacks:

			trigger , args , remove = applied_callback

			
			if args:

				remove( trigger , args = args , nodeClass = node_class )

			else:

				remove( trigger , nodeClass = node_class )
	
		#print '\n>> DEBUG removed applied callbacks for %s' % nbrain.name
			
	

			#print '\t'*2 , 'removed %s [ %s ] ' % ( node_class , trigger.__name__  )




def compute_knobs_and_callbacks( nbrain ):
	

	nbrain.knobs = [ ]

	nbrain.knob_callbacks = { }

	nbrain.system_callbacks = { }

	for tab_path in nbrain.tabs:
		
		#print '??? Generating Knobs from' , tab_path
		
		
		tbrain =  brain.nodeScript.byBasename[ os.path.basename( tab_path ) ] # must exist cause is builded in tab processing
		
		nbrain.knobs.extend( knobs_by_tokenize( tbrain ) )
	
		for k , v  in  __system_callbacks( tbrain ).items() :
		
			if k in nbrain.system_callbacks:
			
				nbrain.system_callbacks[ k ].append( v )
			
			else:
			
				nbrain.system_callbacks[ k ] = [ v ]
			
		for k , v  in  __knob_callbacks( tbrain ).items():

			if k in nbrain.knob_callbacks:

				nbrain.knob_callbacks[ k ].append( v )

			else:

				nbrain.knob_callbacks[ k ] = [ v ]		
		
	#print '   >> computed knobs and callbacks %s' % nbrain.name
	
	
	

def nodeBrain( path , inTab = False ):
	
	'''
	UPDATES STRUCTURE IN brain.nodeScript.Path[ nodeScript file path ] , doesn´t change the brain
	
	Returns a new nodeBrain structure
	
	Everytime this function is called the nodeScript file will be reloaded ( when a new node is created )
	
	This function exposes nbrain into "brain.nodeScript"
		
	'''
	# Simplemente redefinimos el que ya existe o nos devuelve uno nuevo

	nbrain = update_nbrain( path ) # include execution and tab paths normalize
	
	for tab_path in [ x for x in nbrain.tabs if x != nbrain.path ]:

		tab_brain = update_nbrain( tab_path )
		
		#print '\n\t>> DEBUG .... %s tab_brain updated.' % tab_brain.basename
		
			
	compute_knobs_and_callbacks( nbrain )
	
	#print '\n\t.... %s computed knobs and callbacks.' % nbrain.basename
		
	#knobDefault_processing( nbrain )	
	
	#print '\n\t.... %s computed knobDefault values.' % nbrain.basename
	
	
	nbrain.nodeBrain = nodeBrain
	
	return nbrain




def __execute_with_knobs( path ):
	
	# make a cache system per path and per time
	
	#dirname , basename , name, ext = sop.Normalize.split()

	nspace = sop.sh( path )
	
	nspace << brain.Lib.knobs
	
	nspace.DEFAULTS = sop.Brain()

	nspace.__proto__ = sorted( nspace.__dict__.copy().items() )
	
	nspace['exec']
			
	return nspace



#def knobDefault_processing( nbrain ):
#	
#	if hasattr( nbrain.space , 'DEFAULTS' ):
#			
#		for knobname , value in nbrain.space.DEFAULTS.items():
#
#			if type( value ).__name__ in [ 'tuple' , 'list' ]:  # (1,2,3) >> '1 2 3'  
#
#				value = ' '.join( [ str(v) for v in value ] )
#
#			else:
#
#				value = str( value )
#
#
#			route = '.'.join( [ nbrain.name , knobname ] ) # node_class comes from function args
#			
#			print 'Setting knobDefault for %s = %s' % ( route , value )
#			
#			nuke.knobDefault( route , value )



# nodeBrain and support functions
############################################################################################################################################
# libreria







def __system_callbacks( nbrain ):
	
	return __getCallbacks( nbrain.space )[0]


def __knob_callbacks( nbrain ):

	return __getCallbacks( nbrain.space )[1]	
	


def __getCallbacks( nspace ):

	system_callbacks = {}
	knobs_callbacks = {}

	system_callbacks_names = 'onUserCreate onCreate onScriptLoad onScriptSave \
	onScriptClose onDestroy updateUI autolabel beforeRender beforeFrameRender \
	afterFrameRender afterRender knobChanged'.split()

	for name, callback in nspace['user_logic'].items():

		if type(callback).__name__ == 'function':

			if name in system_callbacks_names:

				system_callbacks[name] = callback

			else:
				knobs_callbacks[name] = callback


	return ( system_callbacks , knobs_callbacks )



def knobs_by_tokenize( nbrain ):
		
	bspace =  sop.Brain() << nbrain.space
	
	knobs = []
	
	route = []
	
	names = []
	
	for line in brain.Lib.tokenize2.tokenize_classes( sop.sh( nbrain.path )['read'] ):
		
			
		if line == '[':

			pass
			
		elif line == ']':

			knobs.append(']')

			route.pop()
		
		else:
			
			try:
				
				if len( line ) == 1:
					
					# para pass en una clase de nodescript
					
					continue


				elif line[0][1] == 'class':  # is class

					name = line[1][1]

					route.append( name )

					knobs.append('[')

					knobs.append( nuke.Tab_Knob( name ) )
			
				elif line[1][1] == '=':  # is knob
				
					name = line[0][1]

					route.append( name )

					joined_route = '.'.join( route ) 

					knob = bspace( joined_route , None ) # La ruta debe existir en el espacio y deberia representar un knob
				
					if name in names:
					
						suffix = 1
					
						while 1:
						
							new_name = '%s_%02d' % ( name , suffix ) 
						
							if new_name not in names:
							
								break
						
					
						error_msg = 'ERROR! DUPLICATED KNOB NAME %s' % joined_route
					
						knobs.append( brain.Lib.knobs.errorKnob( new_name , error_msg ) )
				
				
					elif knob and isinstance( knob , nuke.Knob ):

						knob.setName( name )			

						knobs.append( knob )
					
						names.append( name )
				
				
					elif isinstance( knob , sop.Space ):
					
						print 'DEBUG TODO KNOBS INTERFACE WITH SPACE: ' , knob


					else:
					
						error_msg = 'ERROR! WITH ROUTE %s = %s' % ( joined_route , knob )
					
						knobs.append( brain.Lib.knobs.errorKnob( name , error_msg ) )	

					route.pop()
			
			except:
				
				raise RuntimeError , 'problem tokenizing line: %s' % line
				
	return knobs
















