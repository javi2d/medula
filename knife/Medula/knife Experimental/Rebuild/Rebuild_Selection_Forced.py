

# la primera vez this rula, la siguiente estara redefinido por el propio item
		

def thread():
	
	print 'In thread'
	
	for this in space.this.SELECTED_NODES:
		
		print 'into loop' , this.NODE.name()
		
		nuke.executeInMainThreadWithResult( this.NODE.hideControlPanel )	 
	
		nbrain = brain.Lib.nodes7.force_rebuild_node( this )
	
		if nbrain:
		
			callbacks = nbrain.system_callbacks.get( 'onCreate' , [] )
		
			for cb in callbacks:
			
				cb( this )
			
	
		nuke.executeInMainThreadWithResult( this.NODE.showControlPanel )
	
	
		
		

Core.thread( thread ).start()
