



for node in this.SELECTED_NODES:
	
	if node.CLASS == 'Write' and node.VALUES.wm_category == 'Snapshot':
		
		nuke.execute( node.NODE , nuke.frame() , nuke.frame() )
		
	
	
	
	