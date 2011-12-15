
def TASK_online():
	
	return ( True if os.path.isfile( brain.Task.file ) else False )
	
import shutil				


def TASK_error( error  ):
	
	if TASK_online():
		
		shutil.move( brain.Task.file , brain.Task.file.replace( '.task' , '.task.%s' % error ) )
		
		print '\nTASK_ERROR : %s\n' % error
		
		print '\nWaiting for tasks ... '
		
			

def TASK_complete():
	
	if TASK_online():
		
		shutil.move( brain.Task.file , brain.Task.file.replace( '.task' , '.task.done' ) )


def LIB_process_task():

	local_tasks = [ path for path in local._user('Tasks')['$FILES'] if path.endswith('.task') ]
	
	facility_tasks = [ path for path in local.home('Tasks')['$FILES'] if path.endswith('.task') ]
	
	tasks = local_tasks + facility_tasks
	
	
	if tasks:
		
		brain.waiting = False
		
		print '\n>> Process_Task Stage'
		
		print '\n>> %d tasks in queue.' % len( tasks )
		
		brain.Task.file = tasks[0]
		
		brain.Task << sh( brain.Task.file )
		
		return True
	
	
	# If not tasks sleep for n seconds
	
	
	
	return False
		



def LIB_hosts():

	hosts = [ this.HOSTNAME ]

	if brain.Task.hostname and brain.Task.hostname not in hosts:

		hosts.append( brain.Task.hostname )

	return hosts




def LIB_relink_script():
	
	if os.path.exists( brain.Task.script_path ):
	
		return True
	
	else:
	
		print '\n>> Relink_Script Stage\n'

		for host in LIB_hosts():
		
			if not os.path.exists( brain.Task.script_path ):
		
				compatible, match = brain.Lib.sources.compatible_match_cache(  brain.Task.script_path  , host )

				for comp in compatible:

					tmp_script_path = brain.Task.script_path.replace( match , comp )
			
					if os.path.exists( tmp_script_path ):
			
						brain.Task.script_path = tmp_script_path
					
						print 'Sucessful Located Script: %s' % brain.Task.script_path
					
						return True
	
		return False




	

def LIB_relink():
	

	for n in nuke.allNodes():
	
		this = space.this( n )
		
		if this.CLASS == 'Read':
			
			if this.NODE.hasError():

				value  = this.VALUES.file
				
				solved = False
				
				for host in LIB_hosts():
				
					compatible, match = brain.Lib.sources.compatible_match_cache( value , host )
				
					for comp in compatible:
					
						test_path = frame_path = value.replace( match , comp )
					
						print '\nRead test_path : %s \n' % test_path
					
						if '%' in frame_path:
						
							frame_path = frame_path % this.VALUES.first
						
						if os.path.exists( frame_path ):
						
							print 'Relinking Read Node %s : %s >> %s' % ( this.NODE.name() , match , comp )
						
							this.KNOBS.file.setValue( test_path )
						
							solved = True
							
							break
					
					if solved: break
						
							
					
		
		
		elif this.CLASS == 'Write':		
				
			value = this.VALUES.file
			
			solved = False
			
			for host in LIB_hosts():
			
				compatible, match = brain.Lib.sources.compatible_match_cache( value , host )
			
				for comp in compatible:
					
					#print comp
					
					if os.path.exists( comp ) and os.listdir( comp ):
					
						new_value = value.replace( match , comp )
					
						print 'Relinking Write Node %s : %s >> %s' % ( this.NODE.name() , match , comp )
					
						this.KNOBS.file.setValue( new_value )
						
						solved = True
						
						break
		
				if solved: break
				

	#sys.exit()

		

def LIB_load_script():
	
	
	print 'DEBUG' , this.SCRIPT_PATH == brain.Task.script_path
	
	if this.SCRIPT_PATH == brain.Task.script_path:
	
		return True
	
	else:
	
		print '\n>> Load_Script Stage\n'
		
		this.ROOT.KNOBS.name.setValue( '' )

		for n in this.ROOT.ALL_NODES:
			
			nuke.delete( n )
			
		nuke.scriptReadFile( brain.Task.script_path )
		
		this.ROOT.NODE.readKnobs( brain.Task.root )
		
		this.ROOT.KNOBS.name.setValue( brain.Task.script_path )
		

		LIB_relink()
		
		
		
		return True
	
		
		
										

def LIB_locate_node():

	print '\n>> Locate_Node Stage\n'

	output_node = nuke.toNode( 'RENDER_OUTPUT' )

	write_node = ( output_node.input(0) if output_node else None )

	if write_node:
	
		brain.Output.node = write_node
	
		brain.Output.name = write_node.name()
	
		brain.Output.ff   = write_node.firstFrame()
	
		brain.Output.lf   = write_node.lastFrame()
	
		return True
	
	return False




def LIB_build_worker():
	
	print '\n>> Build_Worker Stage\n'
	
	brain.Worker = Brain() << sh( brain.Task.file.replace( '.task' , '.worker' )  )
	
	todo_frames = brain.Worker( 'todo_frames' , [] )
	
	processing_frames = brain.Worker( 'processing_frames' , [] )
	
	done_frames = brain.Worker( 'done_frames' , [] )
	
	if not todo_frames and not done_frames:
		
		todo_frames = range( brain.Output.ff , brain.Output.lf + 1 ) 
		
		if 'tsk_frame_order' in brain.Output.node.knobs():

			frame_order = brain.Output.node.knobs()['tsk_frame_order'].value()
			
			#print 'DEBUG', frame_order
			
			if  frame_order == 'reversed':

				todo_frames.reverse()

			elif frame_order == 'preview':

				todo_frames = preview( brain.Output.ff, brain.Output.lf )

			elif frame_order == 'random':

				random.shuffle( todo_frames )
			
	brain.Worker.todo_frames = todo_frames
	


def LIB_build_render_range():
	
	todo_frames = range( brain.Output.ff , brain.Output.lf + 1 ) 
	
	if 'tsk_frame_order' in brain.Output.node.knobs():

		frame_order = brain.Output.node.knobs()['tsk_frame_order'].value()
		
		#print 'DEBUG', frame_order
		
		if  frame_order == 'reversed':

			todo_frames.reverse()

		elif frame_order == 'preview':

			todo_frames = preview( brain.Output.ff, brain.Output.lf )

		elif frame_order == 'random':

			random.shuffle( todo_frames )
		
		brain.Worker.todo_frames = todo_frames




def LIB_render_frame():
	
	#print '\n'*10
	
	print '\n>> Render_Frame Stage' #, brain.Worker
	
	
	
	worker_file = brain.Task.file.replace( '.task' , '.worker' )
	
	worker_lock_file = worker_file + '.task_lock'
	
	#print 'Debug 1 : ' 
	
	
	while 1:
		
		if os.path.exists( worker_lock_file ):
			
			print '\n [ %s ] Waiting for worker unlock....' % int( time.time() )
			
			time.sleep( .2 )
		
		else:
				
			brain.Worker = Brain() << sh( worker_file  )
			
			while 1:
				
				try:
					
					shutil.copy2( worker_file , worker_lock_file )
					break
					
				except:
					
					time.sleep( .1 )
					
					
					
				#brain.Worker >> sh( worker_lock_file )
			
			#
	
			todo_frames = brain.Worker( 'todo_frames' , [] )
	
			done_frames = brain.Worker( 'done_frames' , [] )
			
			if not todo_frames and not done_frames:
				
				LIB_build_render_range()
			
			#time.sleep( 1 ) # for writing for unlock test
			
			break
			
			
			
			
	undone_frames = [ f for f in brain.Worker.todo_frames if f not in  brain.Worker.done_frames  ]
	
	f = None
	
	if undone_frames:
		
		f = undone_frames[0]
		
		brain.Worker.done_frames.append( f )
		
		brain.Worker >> sh( worker_lock_file  )
		
	
	shutil.move( worker_lock_file , worker_file )
	
	#print 'Debug 2 : ' 
	
		
	
	if f: 
			
		try:
			
			print '\n\nRendering frame : %s ' % f
			
			nuke.execute( brain.Output.node , f , f , continueOnError = True)			
	
		except:
			
			# Add a failed frames list
			
			print '\n\nERROR Rendering frame %s\n\n' % f
			
			#time.sleep( 1 )
		
		
		
	else: # There is not undone frames 		
		
		if TASK_online(): 

			shutil.move( brain.Task.file , brain.Task.file.replace( '.task' , '.task.done') )
			
			print '\n\nTask done. Waiting for tasks...\n'
		


def worker_loop():
	
	
	if LIB_process_task():
		
		if LIB_relink_script():
			
			if LIB_load_script():

				if LIB_locate_node():
					
					LIB_render_frame()
				
				else:
				
					TASK_error( 'unable_to_locate_output_node' )					
				
				#shutil.move( brain.Task.file , brain.Task.file.replace( '.task' , '.task.done') )
				
			else:
	
				TASK_error( 'unable_to_load_script' )
				
		else:

			TASK_error( 'unable_to_reach_script' )
				
	else:
		
		if brain( 'waiting' , False ):
		
			print '\n\nWaiting for tasks... ' % int( time.time() )
			
			brain.waiting = True
			
		time.sleep( 3 )



def start():
	
	medula.local.main( 'worker_space.py' )()
	
	return
	
		
	brain.Lib.database = sh.Lib.database()
	brain.Lib.worker = medula.local.main.Lib.worker()
	
	farm_db = brain.Lib.database.Connection( local.home( 'Farm/Databases/tasks.db' )['file'] )
		
	print farm_db['tasks']	
		
		


def _preview( first_frame, last_frame, array, recursion_level):

	mid_point = ((last_frame - first_frame)//2) + first_frame

	if recursion_level == 0:
		array.append(first_frame)

	array.append(mid_point)
	if recursion_level == 0:
		array.append(last_frame)

	recursion_level = recursion_level + 1

	array_first_half=[]	   
	array_last_half=[]

	if ((mid_point-1)>first_frame):
		_preview(first_frame, mid_point, array_first_half, recursion_level)

	if ((mid_point+1)<last_frame):	
		_preview(mid_point, last_frame, array_last_half, recursion_level)

	max_value = max( len(array_first_half) , len(array_last_half) )
	for element in range (0, max_value):
		if ((element+1)<=len(array_first_half)):
			array.append(array_first_half[element])
		if ((element+1)<=len(array_last_half)):
			array.append(array_last_half[element])



def preview( ff , lf ):

	array = []

	_preview( ff, lf, array, 0)

	return array





	