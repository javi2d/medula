



def solve( path ):
	
	''' This happens when solving a .node file '''
	
	brain.Lib.nodeScript3.remove_applied_callbacks( path )
	
	nbrain = brain.Lib.nodeScript3.nodeBrain( path ) # this will refresh the nbrain
		
	nbrain.applied_callbacks = []
	
	brain.nodeScript( 'byClass' , { } )[ nbrain.name ] = nbrain    # expose in byClass
	
	apply_onUserCreate_onCreate_callback( nbrain )
	
	apply_onKnobCallback_callback( nbrain )
	
	apply_onSysCallback_callback( nbrain )
	
	
	
	return nbrain
	
	
def refresh_node( this ):
	
	'''Refresh the .node and .tab knobs and callbacks definition'''
	
	nbrain = this.CLASS_NBRAIN

	if nbrain:
		
		nbrain = brain.Lib.nodeScript3.nodeBrain( nbrain.path )
		
		#print '\n>> DEBUG Refreshed Node : %s' % nbrain.basename
		
		nbrain.used = False
		
		print '\n&& Refreshed Node :: %s ( %s )' % ( this.NODE.name() , this.CLASS )
		

	return nbrain


def force_rebuild_node( this ):

	nbrain = refresh_node( this )
	
	if nbrain:
		
		remove_nodeScript_knobs( this )

		add_nodeScript_knobs( this )
	
		print '\n\n>> Forced Node Rebuild : %s\n' % this.NODE.name()
	
	return nbrain




def all_custom_knobs( this ):
	
	'''Return current custom knobs in node , included user and nodeScript knobs'''
	
	lenUserKnobs = len( this.NODE.writeKnobs( nuke.WRITE_USER_KNOB_DEFS ).split('\n')[1:] )
	
	return this.SORTED_KNOBS[::-1][ :lenUserKnobs ][::-1]


def user_knobs( this ):
	
	custom_knobs = all_custom_knobs( this )
	
	custom_knobs_names = [ k.name() for k in custom_knobs ]
	
	items = ' '.join( custom_knobs_names ).split( 'END_OF_USER_KNOBS' )[0].strip().split()
	
	return custom_knobs[ :len(items) ]
	
	
def nodeScript_knobs( this ):
	
	custom_knobs = all_custom_knobs( this )
	
	return custom_knobs[ len( user_knobs( this ) ): ]
	


def knob_smc_values( knob ):
	
	single   = ( knob.toScript( None ) if hasattr( knob , 'toScript') else None )
	multiple = ( knob.values() if hasattr( knob , 'values') else [] )
	command  = ( knob.command() if hasattr( knob , 'command') else None )
	
	#if knob.Class() == 'Enumeration_Knob':
	#	msg = '***********DBG value of enumeration knob (  %s = %s )' % ( knob.name(), single )
	#	sys.__stdout__.write( '\n%s\n' % msg )
	
	return single , multiple , command
	
	


def old_values( knobs = [] ): #
	
	current_old_values = {}	
	
	#to_delete_knobs = nodeScript_knobs( this )
	
	if knobs:

		for knob in  [ k for k in knobs if k.Class() not in 'Tab_Knob Link_Knob Text_Knob'.split() ]:
			
			single , multiple , command = knob_smc_values( knob )

			if single or multiple or command:
            
				current_old_values[ knob.name() ] = single , multiple , command

	return current_old_values



	

	
def remove_nodeScript_knobs( this ):
	
	new_knobs_to_add = new_nodeScript_knobs( this )

	current_nodeScript_knobs = user_knobs( this ) + nodeScript_knobs( this ) 
	
	this.CLASS_NBRAIN.old_values = old_values(  current_nodeScript_knobs  )  # harvest the current values of the node knobs
	
		
	for knob in reversed( current_nodeScript_knobs  ):
		
		try:
		
			this.NODE.removeKnob( knob )
	
		except:
			
			pass
			
			#msg = '\nWARNING!!! >> Unable to remove : %s.%s %s' % ( this.NODE.name() , knob.name() , type(knob) )
			
			#sys.__stdout__.write( '\n%s\n' % msg )
	
	
		



	

def add_nodeScript_knobs( this ):
	
	if len( new_nodeScript_knobs( this ) ) == 1: 
			
		return  # only 'END_OF_USER_KNOBS' separator, so nothing to delete

	new_knobs  = new_nodeScript_knobs( this )
	
	for knob in new_knobs:
		
		single , multiple, command = this.CLASS_NBRAIN( 'old_values' ,{} ).get( knob.name() , ( None , None ,None ) )	
		
		if multiple and hasattr( knob , 'setValues'): # Enumeration Knob		
							
			knob.setValues( multiple )
			
			#sys.__stdout__.write( '\n DEBUG >> Restored Multiple Values in %s to %s' % ( knob.name() , multiple ) )

			
		if command and hasattr( knob , 'setCommand'):
			
			knob.setCommand( command )
			
			#sys.__stdout__.write( '\n DEBUG >> Restored Command in %s to %s' % ( knob.name() , command ) )
		
				
		this.NODE.addKnob( knob )
		
		
	
	for knob in new_knobs:
		
		single , multiple, command = this.CLASS_NBRAIN( 'old_values' ,{} ).get( knob.name() , [ None , None ,None ] )	
		
		#single = this.CLASS_NBRAIN( 'knobs_in_conflict' , [] ).get( knob.name() , None )  or single
		
		#sys.__stdout__.write( '\nDEBUG >> Restored Single Value in %s to %s' % ( knob.name() , single ) )
		
		if single:
			
			knob.fromScript( single )
			
			#sys.__stdout__.write( '\nDEBUG >> Restored Single Value in %s to %s' % ( knob.name() , single ) )
			
	
	
	this.CLASS_NBRAIN.old_values = {}
	
	this.CLASS_NBRAIN.used = True
		
	
	
	







		
				

def new_nodeScript_knobs( this ):
	
	
	nodescript_separator = nuke.Text_Knob('END_OF_USER_KNOBS')
	nodescript_separator.setVisible(False)
		
	new_knobs = [ nodescript_separator ]
	
	
	counter = 0
	level = 0
	
	KNOBS = this.CLASS_NBRAIN.knobs[:]

	while KNOBS:

		knob = KNOBS.pop(0)

		if knob == '[':
		
			tab_knob = KNOBS.pop(0)
		
			if level == 0:

				new_knobs.append( tab_knob )		
			
			else:

				new_knobs.append( brain.Lib.knobs.beginGroup( tab_knob.name() )  ) #nuke.Tab_Knob( tab_knob.name() , tab_knob.name() , nuke.TABBEGINGROUP)
		
			level += 1
		

		elif knob == ']':
		
			level -= 1
		
			if level:
			
				counter += 1

				new_knobs.append( brain.Lib.knobs.endGroup( counter ) ) #nuke.Tab_Knob('endGroup%s' % counter, '', nuke.TABENDGROUP)

		else:
			
			new_knobs.append( knob )
	
	
	#if len( new_knobs ) == 1 and this.CLASS == 'Group':
	#	
	#	new_knobs = []
		
	
	
	return new_knobs



def node_needs_rebuild( this ):

	if this.CLASS_NBRAIN( 'used' , False ) or brain( 'AUTO_REFRESH_NODE' , False ):

		refresh_node( this )
	
	new_knobs = [ k.name() for k in new_nodeScript_knobs( this ) ]
	cur_knobs = [ j.name() for j in nodeScript_knobs( this ) ]
	
	#print 'Rebuild ' , new_knobs
	
	if new_knobs == cur_knobs or len( new_knobs ) == 1 :

		return False

	#print '\n\n>> DEBUG node [ %s ] needs rebuild' % this.NODE.name()

	return True


	
	







def apply_onUserCreate_onCreate_callback( nbrain ):

	def trigger():
		
		#print '\n\nON USER_CREATE_ON_CREATE'
		
		if brain( 'KEEP_KNOBS' , False ):

			return
			
		node = space.this.SAFE_NODE #safe_node()
		
		if node:

			# Separar onUserCreate de onCreate , produce dobles
		
			
			this = space.this()
			
			if brain( 'AUTO_REFRESH_NODE' , False ):
				
				refresh_node( this )
			
			#print '\nIn onUserCreate_onCreate TRIGGER CALLBACK : ', this.NODE.name() 
		
			if node_needs_rebuild( this ):
				
				remove_nodeScript_knobs( this )
			
				add_nodeScript_knobs( this )
		
				print '\n&& Rebuilded Node ::', this.NODE.name() 
			


	node_class = nbrain.name

    
	nuke.addOnUserCreate( trigger , nodeClass = node_class )	
    
	nbrain.applied_callbacks.append(  ( trigger , None , nuke.removeOnUserCreate )  )


	nuke.addOnCreate( trigger , nodeClass = node_class )	

	nbrain.applied_callbacks.append(  ( trigger , None , nuke.removeOnCreate )  )



def apply_onKnobCallback_callback( nbrain ):


	def onKnobCallback():

		knob = space.this.SAFE_KNOB  #safe_knob()
		
		if knob:
			
			this = space.this()
			
			if knob.name() in 'xpos ypos selected' and not brain( 'COMPUTE_ALL_KNOBS' , False ):   # 
				
				brain.tmp_counter = brain( 'tmp_counter' , 0 ) + 1
				
				#print '********' , brain.tmp_counter
				
				return
			
			
			if knob.Class() == 'File_Knob' and knob.value():
				
				normalized_value = Normalize.path( knob.value() )
				
				if not normalized_value == knob.value():

					knob.setValue( normalized_value )
				
					#print '\nDEBUG %s File_Knob Normalized : %s\n' % ( knob.name() , knob.value() )
				

			
			
			
			if brain( 'AUTO_REFRESH_NODE' , False ):
				
				refresh_node( this )
			
			
			callbacks = this.CLASS_NBRAIN.knob_callbacks.get( this.KNOB.name() , [] ) # Get the callbacks by knob name


			#if callbacks: print '\n>> DEBUG system_callback trigger with : %s on %s' % ( this.KNOB.name() , this.NODE.name() )
			

			for callback in callbacks:

				callback( this )
			
		


	node_class = nbrain.name	

	trigger = onKnobCallback  #brain.Lib.nodes3_triggers.userCallbacks_Trigger

	nuke.addKnobChanged( trigger , nodeClass = node_class )	

	nbrain.applied_callbacks.append(  ( trigger , None , nuke.removeKnobChanged )  )

	#print '\t'*2 , 'added "GLOBAL knobChanged" on %s node class' % node_class






def apply_onSysCallback_callback( nbrain ):

	def onSysCallback( cbname ):
		
		
		
		node = space.this.SAFE_NODE #safe_node()
		
		if node:
			
			this = space.this()
			
			if cbname == 'knobChanged' and nuke.thisKnob().name() in 'xpos ypos selected'.split() and not brain( 'COMPUTE_ALL_KNOBS' , False ):
				
				#brain.tmp_counter = brain( 'tmp_counter' , 0 ) + 1
				
				return
			

			nbrain = this.CLASS_NBRAIN
			
			
			if brain( 'AUTO_REFRESH_NODE' , False ):
				
				refresh_node( this )
			
			
			callbacks = nbrain.system_callbacks.get( cbname , [] )
			
			

			

			#if callbacks: 
			#	
			#	if cbname == 'knobChanged':
			#	
			#		print '\n>> DEBUG system_callback trigger with : knobChanged.%s on %s' % ( this.KNOB.name() , this.NODE.name() )
			#	
			#	else:
			#	
			#		print '\n>> DEBUG system_callback trigger with : %s on %s' % ( cbname , this.NODE.name() )
		
		
			if cbname == 'autolabel':

				autolabel_combined_result = ''

				for callback in callbacks: 

					result = callback( this )

					if result:

						autolabel_combined_result += result

				return ( autolabel_combined_result or None )


			else:

				for callback in callbacks: 

					callback( this )




	trigger =  onSysCallback #brain.Lib.nodes3_triggers.systemCallback_Trigger


	node_class = nbrain.name	

	for cbname in nbrain.system_callbacks:

		nuke_real_callback = getattr( nuke, 'add' + cbname[0].upper() + cbname[1:], None)
		nuke_real_remove_callback = getattr(nuke, 'remove' + cbname[0].upper() + cbname[1:], None)

		if nuke_real_callback and nuke_real_remove_callback:

			args = ( cbname,  ) 

			nuke_real_callback( trigger , args = args , nodeClass = node_class )

			nbrain.applied_callbacks.append(  ( trigger , args , nuke_real_remove_callback )  )

			#print '\t'*2 , 'added "%s" on %s node class' % ( cbname , node_class )







	

