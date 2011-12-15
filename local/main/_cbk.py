



def knobChanged():
	
	
	if this.KNOB.name() in 'xpos ypos selected'.split():
		
		return 
	
	
	# toolset project load , local._project is redefined 
	project = brain.Lib.project.load_toolset( this )
	
	if project:
		
		print '\nSucessful project toolset load , %s' % project['$NAME']
	
	else:
		
		pass # local._project is not redefined 
		

	
	# Allow knobChanged callback in userNodes
	brain.Lib.userNodes4.knobChanged( this )
	
	
		
		
		
				
				
		
			
			

			
				
				
				
				
	