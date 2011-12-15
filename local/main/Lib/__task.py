
#out = nuke.toNode('ACTIVE_RENDER_OUTPUT')
#
#if out and out.Class() == 'Output':
#	
#	nuke.delete( out )
#
#for n in nuke.selectedNodes():
#	
#	n.setSelected( False )
#	
#
#this.NODE.setSelected( True )
#
#nuke.createNode( 'Output' , 'name ACTIVE_RENDER_OUTPUT' , inpanel = False )


def node( this ):
	

	brain.Lib.script.saveScript()
	
	task_name = os.path.basename( this.VALUES.file ).split('.')[0]
	
	brain.Lib.script.copyScript( '_renderScripts' , script_name = task_name + '.nk' )
	
	task_script_path = brain.Lib.script.copyScript( '_taskScripts' , script_name = task_name + '.nk' , folderize = False )
	

	
		
	brain.Lib.database = sh.Lib.database()
	# interactive
	
			
	local.farm( 'tasks' , 'name TEXT UNIQUE' )  
	# This line always will rebuild the table matching at least query columns
	
	TASK = time.asctime() , task_name, this.HOSTLABEL,  task_script_path , this.NODE.name() , this.NODE.firstFrame() , this.NODE.lastFrame()
	
	local.farm.tasks[ 'date , name , host , path , node , ff , lf' ] = TASK
		

	

def append_render_output( node ):
	
	xpos = node.xpos() + 100
	ypos = node.ypos()
	
	for n in nuke.allNodes():
		
		if n.Class() == 'Output':
			
			nuke.delete( n )
	
	
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
		
		brain.Lib.task.append_render_output( node )
		
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
			
	
