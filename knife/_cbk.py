

def __root_name_changed__():
	
	print '\nA NEW SCRIPT IS ABOUT TO OPEN [...]%s' %  this.VALUE[-30:]
	
	sop.Core.lap( 'script.load' )
	
	project = brain.Lib.project.project_name( this.VALUE )
	
	if project and not project == brain.Project.SCRIPTS:
			
		print '\nLOADING SCRIPTS PROJECT TOOLSET'
		
		local._project = local( 'projects/%s' % project ) 
		
		brain.Lib.include.LOAD_TOOLSET( local._project )
		
		print '\nLOADED PROJECT TOOLSET' , local._project['$PATH']
		
	else:
		
		print 'TODO UNBOUND PROJECT, A PROJECT CANNOT BE UNBOUND'
	
	
	


def knobChanged():
	
	brain.Lib.userNodes4.knobChanged( this )
	
	name = this.KNOB.name()	
		
	if name in 'xpos ypos selected'.split():
			
		return
	
	if not this.SAFE_NODE and this.KNOB and this.KNOB.name() == 'name' and this.VALUE:
		
		__root_name_changed__()
			
	elif this.SAFE_NODE and this.CLASS == 'Root' and this.KNOB and this.KNOB.name() == 'name' and this.VALUE:
		
		__root_name_changed__()
	
		
		
		
		
