


def root_name_changed( self ):

	new_script = None
	
	if self.SAFE_NODE and self.KNOB:
		
		print 'SCRIPT_PATH 1' 
		
		if self.CLASS == 'Root' and self.KNOB.name() == 'name' and self.VALUE:
       
			new_script = self.VALUE
	
	elif self.KNOB:
		
		print 'SCRIPT_PATH 2' 
		
		if self.KNOB.name() == 'name' and self.VALUE:
			
			new_script = self.VALUE
	
	
	return new_script
	
	



def knobChanged():
	
	brain.Lib.userNodes4.knobChanged( this )
	
	name = this.KNOB.name()	
	
	script = this.SCRIPT_PATH
	
	if name in 'xpos ypos selected'.split():
		
		return
	
	
	if not this.SAFE_NODE and this.KNOB and this.KNOB.name() == 'name' and this.VALUE:
		
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
			
		
		
		
		
		
		
	
	#new_script = root_name_changed( this )
	#
	#
	#if new_script == None:
	#	
	#	return
	#	
	#elif new_script:
	#	
	#	sop.Core.lap( 'script.load' )
	#	
	#	print '\nA NEW SCRIPT IS ABOUT TO OPEN'
	#
	#
	#else:
	#	
	#	print '\nSCRIPT NAME CHANGED WITH NO VALUE'
	
	
	
	#elif script and local._project == local.home and local['$PATH'] == medula.local['$PATH']:
	#	
	#	# this will load the project toolset, that happens when
	#	#     - there is a script name
	#	#     - local._project points to the default value local.home
	#	#     - local is other than medula.local
	#	
	#	
	#	print 'GKC 2'
	#	
	#	project = brain.Lib.project.project_name( script )
	#
	#	if project:
	#
	#		local._project = local._project( '../%s' % project ) 
	#	
	#		brain.Lib.include.LOAD_TOOLSET( local._project )
	#
	#		print '\nSucessful project toolset load , %s' % local._project['$NAME']
	#
	#	else:
	#	
	#		print 'TODO UNBOUND PROJECT'
	#
	
		
