

def scan_classy_nodes( root , classes , nodes = [] ):
	
	root.begin()
	
	for n in nuke.allNodes():
		
		if n.Class() in classes:
			
			nodes.append( n )
			
		elif n.Class() == 'Group':
			
			scan_classy_nodes( n , classes , nodes )
			
	return nodes
		
	
nodes = scan_classy_nodes( nuke.Root() ,  [ n.Class() for n in nuke.selectedNodes() ]   )

for node in nodes:

	this_node = this( node )
	
	knobs = this_node.SORTED_KNOBS
	
	print '\n' , this_node.NAME
	
	index = [ k.name() for k in knobs ].index( 'END_OF_USER_KNOBS' ) 
	
	print [ k.name() for k in knobs[:index] ]
	
	for k in reversed( knobs[:index] ):
		
		try:
			
			node.removeKnob( k )
			
		except:
			
			break
	
	knobs = this_node.SORTED_KNOBS
	
	knobs_names = [ k.name() for k in knobs ]
	
	index = knobs_names.index( 'END_OF_USER_KNOBS' )
	
	last_user_knob = knobs[ index - 1 ]
	
	if last_user_knob.Class() == 'Tab_Knob' and 'User' not in knobs_names:
		
		last_user_knob.setName( 'User' )
		last_user_knob.setLabel( 'User' )
		
		
	
	
	


