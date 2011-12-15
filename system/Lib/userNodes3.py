



def update_nbrain( path ):
	
	nbrain = brain.Lib.nodeScript2.nodeBrain( path )
	# get the nbrain of the user node by path
	
	brain.nodeScript( 'byNode' , { } )[ nbrain.name ] = nbrain
	# replace nbrain in dict

	return nbrain



def solve( path ):
	
	'''
	This function is trigger when a .userNode space is called
	
	'''
	
	nbrain = update_nbrain( path )
	

	
	bspace = Brain() << nbrain.space
	# create a brain with space to easy access to attributes
	
	unode_class = bspace( 'Class' , 'NoOp' )
	# get the userNode base class


	UNODE = nuke.createNode( unode_class , 'name %s' %  nbrain.name , inpanel = True )
	# create the userNode
	
	
	this = space.this( UNODE )
	# create a this object with UNODE as context
	

	if unode_class == 'BackdropNode' and this.LAST_SELECTED_NODES:
	# If the userNode is a backdrop compute area
		
		selected_nodes = this.LAST_SELECTED_NODES
		
		minimum = [ min( [ n.xpos() for n in selected_nodes ] ) , min( [ n.ypos() for n in selected_nodes ] ) ]
		maximum = [ max( [ n.xpos() for n in selected_nodes ] ) , max( [ n.ypos() for n in selected_nodes ] ) ]
		
		UNODE.setXYpos( minimum[0]-40 ,  minimum[1]-40 , )
		
		width  = abs( maximum[0] - minimum[0] )
		height = abs( maximum[1] - minimum[1] )
		
		UNODE['bdwidth'].setValue( width + 150 ) 
		UNODE['bdheight'].setValue( height + 120 )
	

	if this.CLASS_NBRAIN:
	# Remove knobs created by .node files in this node Class 
	
		brain.Lib.nodes7.remove_nodeScript_knobs( this )
		
		
	all_custom_knobs = brain.Lib.nodes7.user_knobs( this )
	# Retrieve user knobs
	
	
	if len( all_custom_knobs ) == 1 and all_custom_knobs[0].Class() == 'Tab_Knob':
		
		UNODE.removeKnob( all_custom_knobs[0] )


	Callbacks = nbrain.system_callbacks.get( 'onUserCreate' , [ ] )
	
	for callback in Callbacks:
	# call defined onUserCreate
		
		callback( this )
		
	
		
	for knob in [ k for k in nbrain.knobs if k not in '[ ]'.split() ]:
		
		try:
		
			UNODE.addKnob( knob )
		
		except RuntimeError:
			
			print '\n>> UserNode Duplicated Knob %s\n' % knob.name() 
		
		
		if nbrain.knob_callbacks.get( knob.name() , None ) and hasattr( knob , 'setCommand' ):

			knob.setCommand( 'brain.Lib.userNodes3.button_callback( "%s" , "%s" )' % ( nbrain.name , knob.name() )  )
	
		
	
	id_knob = nuke.String_Knob('userNode_id')
	
	id_knob.setVisible(False)

	id_knob.setValue( nbrain.name )  #nbrain.basename
	
	UNODE.addKnob( id_knob )



	Callbacks = nbrain.system_callbacks.get( 'onCreate' , [ ] )

	for callback in Callbacks:

		callback( this )
		
	
	
	if this.CLASS_NBRAIN:
	
		brain.Lib.nodes7.add_nodeScript_knobs( this )
	
	
	return UNODE , nbrain
	






def refresh_unode( nbrain_name ):
	
	nbrain = brain.nodeScript.byNode[ nbrain_name ]
	
	nbrain = brain.Lib.nodeScript2.nodeBrain( nbrain.path )	
	
	brain.nodeScript.byNode[ nbrain.name ] = nbrain
	
	
	
	
	
def button_callback( nbrain_name , knob_name ):
	
	#print '\n\nunode userCallback' , brain.nodeScript.byNode
	
	#if brain( 'AUTO_REFRESH_NODE' , False ):

		#print '\n&& Refreshed userNode : %s' % nbrain_name
		
	refresh_unode( nbrain_name )
	
	this = space.this( nuke.thisNode() )
	
	knob_callbacks = brain.nodeScript.byNode[ nbrain_name ].knob_callbacks
	
	if knob_name in knob_callbacks:
		
		for callback in knob_callbacks[ knob_name ]:
			
			callback( this )
		
				
				
				