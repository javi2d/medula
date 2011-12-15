



for n in nuke.selectedNodes():
	
	this = space.this( n )
	
	nbrain = this.CLASS_NBRAIN
	
	if nbrain:
		
		brain.Lib.nodes7.refresh_node( this )
		
