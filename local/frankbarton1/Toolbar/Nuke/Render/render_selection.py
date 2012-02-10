

#brain.Lib.mRender.render_selection()


def per_node_execution( this ):
	
	ff = this.NODE.firstFrame() 
	lf = this.NODE.lastFrame()
	
	
	sys.__stdout__.write( '\n\nRendering Node %s ' % this.NODE.name() )
	
	sys.__stdout__.write( '1 ' )
	
	this.KNOBS.wm_refresh.execute()
	
	sys.__stdout__.write( '2 ' )
	
	#nuke.executeInMainThreadWithResult( this.KNOBS.wm_refresh.execute )
			
	if this.VALUES.file:
		
		sys.__stdout__.write( '3 ' )
		
		print '\n>> Executing IN FULL RESOLUTION : %s , [ %s , %s ]' % ( this.NODE.name() , ff ,lf )
		
		nuke.executeInMainThreadWithResult( this.ROOT.KNOBS.proxy.setValue , ( False , )  )
		
		
		
		nuke.execute( this.NODE , ff, lf , continueOnError = True ) 
		
		sys.__stdout__.write( '3.1 ' )
		
	if this.VALUES.proxy:
		
		sys.__stdout__.write( '4 ' )
		
		nuke.executeInMainThreadWithResult( this.ROOT.KNOBS.proxy.setValue , ( True , )  )
		
		this.KNOBS.wm_overwrite.setValue( True )
		this.KNOBS.wm_refresh.execute()

		print '\n>> Executing IN PROXY RESOLUTION : %s , [ %s , %s ]' % ( this.NODE.name() , ff ,lf )

		nuke.execute( this.NODE , ff, lf , continueOnError = True )
		
		this.KNOBS.wm_refresh.execute()
		
		sys.__stdout__.write( '4.1 ' )
		


current_proxy_mode = this.ROOT.VALUES.proxy

for n in nuke.selectedNodes():
	
	this_node = this( n )
	
	current_overwrite_value = this_node.VALUES.wm_overwrite
		
	this_node.BRAIN.afterRenderUpdate = False
		
	try:
		
		per_node_execution( this_node )
	
	except:
		
		raise

	finally:

		this_node.KNOBS.wm_overwrite.setValue( current_overwrite_value )
		this_node.BRAIN.afterRenderUpdate = True


this.ROOT.KNOBS.proxy.setValue( current_proxy_mode )