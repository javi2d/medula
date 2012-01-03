
############################################################################################################################################
# nodeBrain and support functions










def knobDefault_processing( nbrain ):
	

	if hasattr( nbrain.space , 'DEFAULTS' ):

		for knobname , value in nbrain.space.DEFAULTS.items():

			if type( value ).__name__ in [ 'tuple' , 'list' ]:  # (1,2,3) >> '1 2 3'  

				value = ' '.join( [ str(v) for v in value ] )

			else:

				value = str( value )


			route = '.'.join( [ nbrain.name , knobname ] ) # node_class comes from function args

			nuke.knobDefault( route , value )




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
		
		nbrain = brain.nodeScript.byBasename[ basename ] = Brain()
	
		
	nbrain.path = path

	nbrain.name = name
	
	nbrain.basename = basename 
	
	nbrain.ext  = ext

	nbrain.shell = sh( dirname )
	
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
		
		nbrain.knobs.extend( __knobs( tbrain ) )
	
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
	

	# base structure
	
	nbrain = update_nbrain( path ) # include execution and tab paths normalize
	
	#print '\n>> DEBUG .... %s class_brain updated.' % nbrain.basename
	
	#print '\n\t.... %s nbrain updated.' % nbrain.basename
	
	for tab_path in [ x for x in nbrain.tabs if x != nbrain.path ]:

		tab_brain = update_nbrain( tab_path )
		
		#print '\n\t>> DEBUG .... %s tab_brain updated.' % tab_brain.basename
		
		
	compute_knobs_and_callbacks( nbrain )
	
	#print '\n\t.... %s computed knobs and callbacks.' % nbrain.basename
		
	knobDefault_processing( nbrain )	
	
	#print '\n\t.... %s computed knobDefault values.' % nbrain.basename
	
	
	nbrain.nodeBrain = nodeBrain
	
	return nbrain


		


'''


'''




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



def __knobs( nbrain ):
	
	#print '\n\n\n\n%s\n' % nbrain.path
	
	
	#print 'getCOmbined'
	
	#print 'processing file   %s' % ( nbrain.name + nbrain.ext )
	
	#lines  = __stage0_Isolate_Classes( nbrain.path )
	
	#print 'generated lines %s : %s' % ( nbrain.name , lines )
	
	#result = __stage1_Process_Lines( lines )

	#knobs  = __stage2_Process_Result( result , nbrain.space )
	
	
	knobs_token = knobs_by_tokenize( nbrain.path , nbrain.space )
	
	#print '\n*******BY TOKENIZE KNOBS\n\n%s\n\n' %  knobs_token
	
	

	#return knobs

	return knobs_token


def knobs_by_tokenize( path , nspace ):
	

	#isPath = os.path.basename( path ).startswith( 'Convertor_v02' )
		
	knobs = []

	route = []

	active = False
	
	level = 0

	bspace =  Brain() << nspace

	opened_tabs = 0

	names = []
	
	
	
	for line in brain.Lib.tokenize.tokenize_classes( sh( path )['read'] ):
		

		
		if active and level == 0 :
			
			active = False
			
			route = []
		

		if line == '[':

			pass

		elif line == ']':

			if opened_tabs:

				level -= 1

				knobs.append(']')

				opened_tabs -= 1
				
				route.pop()

		else:
			
			
			
			isClass = line[0][1] == 'class'
			
			isVar = line[1][1] == '='
			

			if isClass:

				level += 1

				active = True

				name = line[1][1]

				route.append( name )

				knobs.append('[')

				knobs.append( nuke.Tab_Knob( name ) )

				opened_tabs += 1

			
			elif active and isVar:

				name = line[0][1]

				route.append( name )

				joined_route = '.'.join( route ) 


				knob = bspace( joined_route , None ) # La ruta debe existir en el espacio y deberia representar un knob

				if knob and isinstance( knob , nuke.Knob ):

					knob.setName( name )			

					knobs.append( knob )
					
					names.append( name )
					
					# ??? MIRAR SI HAY NOMBRES DUPLICADOS Y PONER UN ERROR KNOB
					

				else:
					
					error_msg = 'ERROR! WITH ROUTE %s = %s' % ( joined_route , knob )
					
					knobs.append( brain.Lib.knobs.errorKnob( name , error_msg ) )	


				route.pop()
			

			


	for i in range( opened_tabs ):
		
		knobs.append(']')
	
	return knobs






def __execute_with_knobs( path ):
	
	
	
	# make a cache system per path and per time

	dirname , basename = os.path.split( path )
	name, ext = os.path.splitext( basename )

	#nspace = sh( '' )
	
	
	nspace = sh( path )
	
	nspace << brain.Lib.knobs
	
	#print nspace['info']
	
	nspace.__proto__ = sorted( nspace.__dict__.copy().items() )
	
	nspace['exec']
		
	#nspace = Core.execution( path , nspace )  #This function executes and set __called__
	
	#print '****' , nspace['info']
	
	#brain.nscript[ path ].space = nspace

	#print '3 DEBUG EOF Core.execution' , nspace
	
	#print '\n\t.... Reloaded file with knobs: %s' % basename
	
	return nspace




def __stage0_Isolate_Classes( path ):
	
	#print '+++++++++ %s' % path
	
	f = open( path )

	lines = [ l for l in f.readlines() if ( l.strip() and not l.strip().startswith('#') ) ]  #and ) ]
	
	#print '+++++++++ %s' % line
	
	f.close()

	isolated_lines = []

	add = False

	last_level = 0

	for line in lines:
		
		
		
		lstrip_line = line.lstrip()
		level = len(lstrip_line) - len( line )

		if level == 0 and line.startswith( 'class' ):
			add = True

		elif level == 0 and not line.startswith( 'class' ):
			add = False


		if add:

			if ( '=' in line or 'class' in line):

				isolated_lines.append( line )

				#print line


	return isolated_lines



def __stage1_Process_Lines( lines  ):

	def process_line( line ):

		strip_line = line.rstrip()

		tab_varname = strip_line.split( '=' )[0].rstrip()

		varname     = tab_varname.strip()

		level =  len(tab_varname) - len( varname )

		if varname.startswith('class'):

			varname  =  varname[5:].replace(':' , '').strip()

		#print level , tab_varname

		return level , varname


	last_level = 0	

	result = []

	step = 0

	valid = False

	opened_groups = 0

	for line in lines:

		level , varname = process_line( line )

		if level == 0 : #and varname != 'knobDefault':

			valid = True

		elif level == 0:

			valid = False

		if not valid:

			continue

		if last_level == 0:			
			step = level

		if level == last_level:

			result.append( '%s' % varname )	

		elif level > last_level:

			last = result.pop()

			result.append( '[' )

			opened_groups += 1

			result.append( '%s' % last )
			result.append( '%s' % varname )	

		elif level < last_level:


			result.append( ']' )
			opened_groups -= 1

			jump = ( last_level/step )-( level/step ) 

			if jump > 1:

				#print '???JUMPS' , jump

				for i in range( jump-1):

					##NEW!!!! , before was flat

					result.append( ']' )
					opened_groups -= 1	

			result.append( '%s' % varname )	

		last_level = level	

	for i in range( opened_groups ):

		result += ']'

	return result




def __stage2_Process_Result( result , nspace ):
	
	# route 
	
	route = []

	add_to_route = False

	prev_name = None

	knobs = []

	bspace =  Brain() << nspace	
	
	for name in result:

		#print '++ %s ' % name 

		if name == '[':

			knobs.append( '[' ) #nuke.BeginTabGroup_Knob('[')

		elif name == ']':

			route.pop()
			knobs.append( ']' ) #nuke.EndTabGroup_Knob(']')


		elif prev_name == '[':

			route.append( name )
			knobs.append( nuke.Tab_Knob( name ) )

		else:
			
			# ruta para el atributo del espacio
			
			route.append( name )
			
			joined_route = '.'.join( route ) 
			
			
			knob = bspace( joined_route , None ) # La ruta debe existir en el espacio y deberia representar un knob

			if knob and isinstance( knob , nuke.Knob ):
					
				knob.setName( name )			
				
				knobs.append( knob )
				
			else:
				
				knobs.append( brain.Lib.knobs.errorKnob( name ) )
				
				#raise AttributeError( 'Invalid Knob' )
			
			route.pop()

		prev_name = name
	
	
	print '\n\n**REGULAR KNOBS\n%s\n\n' % knobs	
	
	return knobs







