




def thread( steps = 100 ):
	
	zoom_level = 1
	
	for i in range( steps ):
		
		time.sleep( .01 )
		
		zoom_level = nuke.zoom() - .1
		
		print zoom_level
		
		if zoom_level > 0:
		
			nuke.executeInMainThreadWithResult( nuke.zoom , ( zoom_level , ) )
 			
		

Core.thread( thread ).start()