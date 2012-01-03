

def __root_name_changed__():
	
	print '\nOPENING A NEW SCRIPT [...]%s' %  this.VALUE[-100:]  #  This function is trigger when 'this' is bound to Root.name
	
	sop.Core.lap( 'script.load' ) # Lapse closed in Root.onCreate
	
	script_path = Normalize.path( this.VALUE )
	
	brain.Lib.sources.normalize()
	
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
		
		print '\n\n!!!!!!!! PROJECT NOT FOUND, CHECK Sources.memory or knife/_cbk.py/__root_name_changed__() to review the problem'
	


def knobChanged():
	
	brain.Lib.userNodes4.knobChanged( this )
	
	name = this.KNOB.name()	
		
	if name in 'xpos ypos selected'.split():
			
		return
	
	if not this.SAFE_NODE and this.KNOB and this.KNOB.name() == 'name' and this.VALUE:
		
		__root_name_changed__()
			
	elif this.SAFE_NODE and this.CLASS == 'Root' and this.KNOB and this.KNOB.name() == 'name' and this.VALUE:
		
		__root_name_changed__()
	
		
		
		
		
