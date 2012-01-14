


def knobChanged():
	
	#brain.Lib.userNodes4.knobChanged( this )  # moved to system/_cbk.py
	
	if this.KNOB.name()	 in 'xpos ypos selected'.split():
			
		return
	
	cond1 = ( not this.SAFE_NODE and this.KNOB and this.KNOB.name() == 'name' and this.VALUE )
	
	cond2 = ( this.SAFE_NODE and this.CLASS == 'Root' and this.KNOB and this.KNOB.name() == 'name' and this.VALUE )
	
	if cond1 or cond2:
		
		#  This is trigger when 'this' is bound to Root.name
		
		print '\nRoot.name changed to : [...] %s' %  this.VALUE[-75:]  
	
		sop.Core.lap( 'script.load' ) # Lapse closed in Root.onCreate
	
		script_path = Normalize.path( this.VALUE )
	
		#brain.Lib.sources.normalize()
	
		match = None
	
		for H , HN , R , LR , RR  in  brain.Lib.sources.walk():
		
			if HN.lower() == this.HOSTNAME.lower():
			
				paths_to_test = LR + RR
			
			else:
			
				paths_to_test = RR
						
			for resource in paths_to_test:
			
				if script_path.startswith( resource ):

					match = resource
				
					break
	
		if match:
		
			project_name = script_path.replace( match + '/' , '' ).split('/')[0] # first 
	
			print '\nPROJECT FOUND = ' , project_name
	
		else:
		
			print '\nPROJECT NOT FOUND !'
	
		
		
		
