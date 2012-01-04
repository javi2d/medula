


'''
MANAGED READS UTILS

Used at least by Managed_Read.py , the 'R' key replacement

'''


def LIB_read_creator_thread( read_nodes_params ):

	print '\nQueued %s read nodes' % len( read_nodes_params )
	
	
	
	for seq_path , ff, lf in read_nodes_params:
		
		print '\n>> %s %s-%s' % ( seq_path , ff, lf )
		
		_ , ext = os.path.splitext( seq_path )
		
		isStill = False
		
		if ff == lf == None:
			
			isStill = True
			
			ff = lf = 1
		
		if ext in brain.Exclusions( 'excluded' , [] ):
			
			continue

			
		elif ext in '.mov'.split():

			for i in range( ff, lf + 1 ):
				
				print '\n>> Solved as MovieClip file '
				
				if '%' in seq_path:
				
					single_file = seq_path % i
					
				else:
					
					single_file = seq_path
				
				node = this( nuke.createNode('Read' , inpanel = False ) )
			
				node.KNOBS.file.fromUserText( single_file )
				
				node.NODE.setSelected( False )
			
			
		elif ext in '.obj'.split():
			
			print '\n>> Solved to ReadGeo'
			
			node = this( nuke.createNode('ReadGeo' , inpanel = False ) )
			
			node.KNOBS.file.fromUserText( seq_path )
			
			node.NODE.setSelected( False )
			
		elif ext in '.fbx'.split():
			
			print '\n>> Solved to FBX scene '
			
			scene = this( nuke.createNode('Scene' , inpanel = False ) )
			
			node = this( nuke.createNode('ReadGeo' , inpanel = False ) )
			
			node.KNOBS.file.fromUserText( seq_path )
			
			node.NODE.setSelected( False )
			
			scene.NODE.setInput( 0 , node.NODE )
			
			node = this( nuke.createNode('Camera2' , inpanel = False ) )
			
			node.KNOBS.read_from_file.setValue( True )
			
			node.KNOBS.file.setValue( seq_path ) 
			
			node.NODE.setSelected( False )
			
			scene.NODE.setInput( 1 , node.NODE )
			
			scene.NODE.setSelected( False )
			
			
		else:
			
			print '\n>> Solved to Regular Read Node '
			
			node = this( nuke.createNode('Read' , inpanel = False ) )
			
			if isStill:
				
				node.KNOBS.file.fromUserText( seq_path )
				
			else:
				
				node.KNOBS.file.fromUserText( '%s %s-%s' % ( seq_path , ff, lf ) )

			
			node.NODE.setSelected( False )
	
	

def LIB_recursive_read_creator( folder , pattern = None , recursive = True ):
		
	read_nodes_params = []
	
	for P,D,F in os.walk( folder ):

		D[:] = [ d for d in D if not d.startswith( '.' ) and not d.startswith( '__' ) ]
		
		mov_files = [ [ Normalize.join( P , f )  , None , None ] for f in F if os.path.splitext( f )[1].lower() == '.mov'  ]
		
		read_nodes_params.extend( mov_files )
		
		seq = brain.Lib.sequence.sequences( P )
		
		for name , stats in sorted( seq.items() ) :
			
			fname, ext = os.path.splitext( name )
			
			if ext.lower() == '.mov':
				
				continue
			
			if '.PROXY' in name:
				
				continue
				
			ff, lf, cont = stats
			
			seq_path = Normalize.join( P , name )
		
			params = [ seq_path , ff, lf ]

			read_nodes_params.append( params )
			
			
		if not recursive:
			
			break
		
	
	if pattern:
		
		import fnmatch
		
		read_nodes_params = [ param for param in read_nodes_params if fnmatch.fnmatch( os.path.basename( param[0] ).lower() , pattern.lower() ) ]

		
	nuke.executeInMainThreadWithResult( LIB_read_creator_thread , ( read_nodes_params , ) )
	


def getClipname( default = None ): #, this = space.this  
	
	clip_names = nuke.getClipname( 'Managed Read File(s)' , default = default , multiple = True )

	if not clip_names:
		
		print '>> Cancelled Managed Read Files Browser'
		return

	for value in clip_names:
		
		if os.path.isdir( value ):
			
			LIB_recursive_read_creator( value , pattern = None , recursive = True )
		
		elif '*' in value:
			
			dirname , basename = os.path.split( value )
			
			LIB_recursive_read_creator( dirname , pattern = basename , recursive = True )

		else:
			
			parts = value.split()
			
			frange = parts[-1]
			
			if '-' in frange and frange.split('-')[0].isdigit() and frange.split('-')[1].isdigit():
				
				seq_path = ' '.join( parts[:-1] )
				
				ff , lf = [ int( x ) for x  in  frange.split('-') ]
				
			else:
				
				seq_path = value
				
				ff , lf = None , None
				

			LIB_read_creator_thread( [ [ seq_path , ff , lf ] ] )

	


def read_from_write( this ):
	
	path = this.VALUES.file
	
	if not this.VALUES.wm_category == 'disabled' and not this.VALUES.wm_overwrite:

		import re 
	
		matches = re.findall( "_v\d+" , path, re.IGNORECASE)
	
		if matches:
		
			digits = matches[-1][2:]
		
			version_padding = '_v%' + str( len ( digits ) ).zfill( 2 ) + 'd'
			
			version = ( ( int(digits) - 1 ) or 1 )
			
			path = path.replace( matches[-1] , version_padding %  version )
	
	
	first_frame = this.NODE.firstFrame()
	last_frame = this.NODE.lastFrame()
	
	node = this( nuke.createNode('Read', inpanel = False )  )

	node.KNOBS.file.fromUserText( path )
	
	if '%' in path:

		for name in 'first origfirst'.split():
			node.KNOBS( name ).setValue( first_frame )

		for name in 'last origlast'.split():
			node.KNOBS( name ).setValue( last_frame )

	node.NODE.setXYpos( this.NODE.xpos() , this.NODE.ypos() + 100 )

	return node

	
	

def read_from_read( read_node ):
	
	file_value = read_node['file'].value()

	if not file_value and 'proxy' in read_node.knobs():

		file_value = read_node['proxy'].value()

	dirname , basename = os.path.split( file_value )
	
	#if os.path.exists( dirname ):
	#	
	#	os.listdir( dirname )
	
	
	getClipname( default = dirname + '/' )
	
	



def read_from_selection():
	
	# Define behaviour to create Read Nodes from other nodes
	
	selected_nodes = nuke.selectedNodes()
	

	# NO NODES SELECTED

	if len( selected_nodes ) == 0:

		print '>> Managed Read, no Nodes selected'

		getClipname()

		
	else:
		
		matches = 0
		
		for n in selected_nodes:
			
			this = space.this( n )
			
			matches += 1
			
			if this.CLASS == 'Write':
				
				read_from_write( this )
			
			elif this.CLASS == 'Read' and len( selected_nodes ) == 1:
				
				read_from_read( n )
			
			
			elif this.CLASS == 'Read':
				
				n['reload'].execute()
				
			else:
				
				matches -= 1
				
			
			if not matches:
				
				getClipname()
				
			

			

			
			

#
#def read_from_ingest( ingest_node ):
#	
#	write_node = this( ingest_node ).NODES.Write1
#		
#	new_node = read_from_write( write_node )
#	
#	this_ingest = this( ingest_node )
#	
#	new_node.NODE.setXYpos( this_ingest.NODE.xpos() , this_ingest.NODE.ypos() + 100 )






		
		
		
			
	
	
	
	



	
	
