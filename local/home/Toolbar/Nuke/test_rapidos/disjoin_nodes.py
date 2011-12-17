


selected = this.SELECTED_NODES

if not selected:
	
	nuke.message( 'select some nodes to disjoin' )
	raise RuntimeError , 'no nodes selected'


for this in selected:
	
	this.NODE.setInput( 0 , None )
	
	#print dir( this.NODE )
