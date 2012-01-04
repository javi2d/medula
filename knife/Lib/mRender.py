

#print 'Debug RELOADED mRender.py'


def _execute( node , proxy_mode ):
	
	root = this.ROOT
	
	current_proxy_mode = root.VALUES.proxy
	
	root.KNOBS.proxy.setValue( proxy_mode )
	
	mode = ( 'FULL' if proxy_mode == False else 'PROXY' )
		
	ff = node.firstFrame() 
	lf = node.lastFrame()
	
	print '\n>> Executing in %s RESOLUTION : %s , [ %s to %s ]' % ( mode , node.name() ,  ff ,lf )
	
	nuke.execute( node , ff, lf , continueOnError = True )
	
	print '\n<< Executing in %s RESOLUTION : %s , [ %s to %s ]\n' % ( mode , node.name() , ff ,lf )
	
	root.KNOBS.proxy.setValue( current_proxy_mode )
	

def process_autowrites():
	
	for n in nuke.selectedNodes():
		
		this_node = this( n )
		
		if this_node.VALUES.file_type == ' ':
			
			_execute( n , True )
			
		else:
			
			_execute( n , False )
	



def selection_in_full( check_knobs = True ):
	
	if check_knobs:
	
		will_fail_nodes = [ n for n in nuke.selectedNodes() if not n['file'].value()  ]

		if will_fail_nodes:
		
			nuke.message( 'Please review "file" knob on these nodes\n<center>%s</center>\nCommand cannot be processed' % [ n.name() for n in will_fail_nodes ] )
			return
	
	for n in nuke.selectedNodes():
		
		_execute( n , False )


def selection_in_proxy( check_knobs = True ):
	
	if check_knobs:
	
		will_fail_nodes = [ n for n in nuke.selectedNodes() if not n['proxy'].value()  ]

		if will_fail_nodes:
		
			nuke.message( 'Please review "proxy" knob on these nodes\n<center>%s</center>\nCommand cannot be processed' % [ n.name() for n in will_fail_nodes ] )
			return
	
	for n in nuke.selectedNodes():
	
		_execute( n , True )
	

	

		

def task_node( this ):
	
	task_name = os.path.basename( this.VALUES.file ).split('.')[0]
	
	task_script_path = 'asdasdsa'
	
	
	TASK = time.asctime() , task_name, this.HOSTLABEL,  task_script_path , this.NODE.name() , this.NODE.firstFrame() , this.NODE.lastFrame()

	
	# interactive
	
	farm = this.FARM
	
	
	#farm.DROP('*')

	farm.CREATE(  'tasks' , 'date TEXT , task TEXT UNIQUE , host TEXT , script TEXT, node TEXT, ff INT , lf INT'  )
	
	farm.INSERT( 'tasks' , TASK )

	print farm.SELECT_ALL( 'tasks' )
	
	
	
	#brain.Lib.script.saveScript()
	#
	#task_name = os.path.basename( this.VALUES.file ).split('.')[0]
	#
	#brain.Lib.script.copyScript( '_renderScripts' , script_name = task_name + '.nk' )
	#
	#task_script_path = brain.Lib.script.copyScript( '_taskScripts' , script_name = task_name + '.nk' , folderize = False )
	
	
	
		

		

	

def append_render_output( node ):
	
	xpos = node.xpos() + 100
	ypos = node.ypos()
	
	render_output_node = nuke.toNode( 'RENDER_OUTPUT' )
	
	if render_output_node:
		
		nuke.delete( render_output_node )

	output = nuke.nodes.Output( name = 'RENDER_OUTPUT' , xpos = xpos , ypos = ypos  )
	
	output.setInput( 0 , node )


def copyTask( target , task_name = None ):
	
	#target = ( target if  type( target ).__name__ == 'Shell'  else getattr( main , target ) )
	
	task_name = ( task_name if task_name.endswith('.task') else task_name + '.task' )
	
	
	target_task_folder = target['$PATH'] #target( '__tasks' )['$PATH']
	
	import glob
	
	#matches = glob.glob( '%s/*%s' % ( target_task_folder , task_name ) )
	
	matches = glob.glob( '%s/*.task*' %  target_task_folder ) #( target_task_folder , task_name ) )
	
	index = 0
	
	if matches:
		
		last_item = sorted( matches )[-1]
		
		#print 'copyScript DEBUG2' , last_item 
		
		basename = os.path.basename( last_item )
		
		prefix = basename.split('_')[0]
		
		if prefix.isdigit():
			
			index = int( prefix )
			
	target_task_path = '%s/%04d_%s' % ( target_task_folder , index + 1 , task_name )
	
	brain.Task >> sh( target_task_path )
	
	return target_task_path
	
	
	
	
def append_render_output_and_task( node , target ):
	
	#target = ( target if  type( target ).__name__ == 'Shell'  ) #else  getattr( main , target )  
	
	if target and node.Class() in 'Write'.split() and node['file'].value():
		
		append_render_output( node )
		
		brain.Lib.script.saveScript() # this will upgrade subversion, in fact render any node will update subversion
		
		render_name = os.path.basename( node['file'].value() ).split('.')[0]
		
		brain.Lib.script.copyScript( '_renderScripts' , script_name = render_name + '.nk' )
		
		task_script_path = brain.Lib.script.copyScript( '_taskScripts' , script_name = render_name + '.nk' , folderize = False )
		
		
		# Task content build
		
		brain.Task = Brain()
		
		brain.Task.script_path = task_script_path
		
		brain.Task.hostname = this.HOSTNAME
		
		brain.Task.root = this.ROOT.NODE.writeKnobs( nuke.WRITE_ALL | nuke.TO_VALUE | nuke.TO_SCRIPT ) #
		
		
		# Is this necessary??
		
		compatible , match = brain.Lib.sources.compatible_match( task_script_path )

		for test_path in compatible:

			tmp_path = brain.Task.script_path.replace( match , test_path )
	
			if os.path.isfile( tmp_path ):
	
				brain.Task.script_path = tmp_path
				
				print '\n>> Sucessfully relinked nuke script path'
				
				break

		
		
		task_path = copyTask( target , render_name )
		
		return task_path
	
	else:
		
		# poner avisos de no implementacion
		
		return ''
			
	
	
		
		
		
		