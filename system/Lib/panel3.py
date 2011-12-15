
def get_nbrain( path ):
	
	

	if nbrain:
		
		return [ nbrain , False ]
	
	else:
		
		return [ brain.Lib.nodeScript2.nodeBrain( path ) , True ]
		


class Static_Panel( object ):
	
	def __init__( self , path ):
		
		self.path = path
		
		self.nbrain = Dynamic_Panel( self.path ).nbrain
		
		#print '\n	Registering Panel : %s' % self.nbrain.name
		
		nukescripts.registerPanel( self.nbrain.name , self.panel   ) 

		nuke.menu('Pane').addCommand( self.nbrain.name , self.show  ) 
	
	
	def panel( self ):
		
		panel , node , widget = self.nbrain.static_bundle
		
		return panel
	
	
	def show( self ):
		
		pane = nuke.thisPane()
		
		pane.add( self.panel() )
			
		return self.panel()

	



class Dynamic_Panel(object):
	
	def __init__( self , path , update = True ):
		
		self.nbrain = brain.nodeScript( 'byBasename' , {} ).get(  os.path.basename( path ) , None )
		
		self.path = path

		if not self.nbrain:
			
			self.update_nbrain()
			
			self.build_panel()
		
			self.apply_callbacks()
		
			self.nbrain.static_bundle = self.nbrain.dynamic_bundle
		

	
		
	def hide( self ):
		
	
		dialog , node , widget = self.nbrain.dynamic_bundle
		
		dialog.hide()
		
		print dir( dialog )
		
	
			
	def show( self ):		
		

		self.update_nbrain()
		
		panel = self.build_panel()
	
		self.apply_callbacks()		

		panel.show()
		
		return panel
	
	
	def showModal( self ):
		
		self.update_nbrain()
		
		panel = self.build_panel()
		
		self.apply_callbacks()
		
		panel.showModal()
		
		return panel
			

		
	

	def update_nbrain( self ):
		
		
		self.nbrain = brain.Lib.nodeScript2.nodeBrain( self.path ) # always return the same structure, updated
		
		applied_callbacks = self.nbrain( 'applied_callbacks' , [] )

		for applied_callback in applied_callbacks:

			trigger , args , remove = applied_callback	
			remove( trigger , args = args , nodeClass = 'PanelNode' )


		self.nbrain.applied_callbacks = []		
		


		byPanel = brain.nodeScript( 'byPanel' , {} )

		byPanel[ self.nbrain.name ] = self.nbrain


	
	def build_panel( self ):
		
		
		import pyui
		
		class Dialog( pyui.Dialog ):
			
			def show( self ):
				
				super( Dialog, self ).show()		
			
			def hide( self ):
				
				super( Dialog, self ).hide()
		
		
		old_widget = None
		
		if self.nbrain( 'dynamic_bundle' , None ):
			
			panel , old_node , old_widget  = self.nbrain.dynamic_bundle
			
			old_widget.hide()
			
		else:

			panel = Dialog( self.nbrain.name.replace( '_' , ' ' ) , self.nbrain.name ) #pyui.
		
		
		node  = nuke.PanelNode() 
		
		
		self.runCallback( 'onUserCreate' , panel , node)
		
		# autogestionar nombres duplicados
		
		for knob in self.getNewKnobs():

			try:
				
				node.addKnob( knob )
			
			except RuntimeError:
				

				print '\n>> WARNING! Error while adding %s knob to %s panel node. Usually knob name is duplicated.' % ( knob.name() , self.nbrain.name )
		
		
		widget = node.createWidget( panel )
		
		panel.add( widget , 0, 0, 1, 3)	
		
		self.nbrain.dynamic_bundle = panel , node , widget
		
		self.runCallback( 'onCreate' , panel , node)
		
		if old_widget:
			
			old_widget.destroy()
		

		print '\nDEBUG : Recreated Panel %s' % self.nbrain.name

		return panel
		
		
	def getNewKnobs( self ):

		def isTab( obj ):

			return  type( obj ).__name__ == 'Tab_Knob'


		prev_item = None

		is_first_tab = True

		KNOBS = [ ]


		for item in self.nbrain.knobs[1:-1]:

			if item == '[' and prev_item == ']':

				KNOBS.pop()

			elif item == '[':

				KNOBS.append( nuke.BeginTabGroup_Knob() )

			elif item == ']':

				KNOBS.append( nuke.EndTabGroup_Knob() )

			else:

				if is_first_tab and isTab( item ) and item.name() == 'User':

					is_first_tab = False

				else:

					KNOBS.append( item )
					item.setFlag( nuke.NO_UNDO | nuke.NO_ANIMATION )


			prev_item = item

		id_knob = nuke.String_Knob('panel_id')

		id_knob.setVisible(False)

		id_knob.setValue( self.nbrain.name )

		KNOBS.append( id_knob )

		return KNOBS
	
	
	def apply_callbacks( self ):
		
		self.apply_onKnobCallback_callback()
		self.apply_onSysCallback_callback() # must exclude onCreate and userCreate????
	
		
	def runCallback( self , tag ,  panel , node):
		
		callbacks = self.nbrain.system_callbacks.get( tag , [] )

		this = space.this( node )

		this.PANEL = self #panel
		
		this.DIALOG = panel
		
		for callback in callbacks:

			callback( this )	
		
	
	def refresh_panel( self ):
		
		self.update_nbrain()
		self.apply_callbacks()
		
		print '\n&& Refreshed Panel : %s' %  self.nbrain.name


	def apply_onSysCallback_callback( self ):

		def onSysCallback( panel_id  , cbname ):
			
			this = space.this() # current context, this.NODE is well defined
			
			nbrain = brain.nodeScript.byPanel[ panel_id ]
			
			this.PANEL = self
			
			this.DIALOG , node , this.WIDGET = nbrain.dynamic_bundle
			
			
			if this.KNOBS( 'panel_id' , None , create_att = False ) and this.VALUES.panel_id == node.knobs()['panel_id'].value():
				
				if brain( 'AUTO_REFRESH_NODE' , False ) and not cbname == 'knobChanged' :
					
					self.refresh_panel()
					
				callbacks = nbrain.system_callbacks.get( cbname , [] )

				for callback in callbacks:
					
					callback( this )
			


			

		trigger = onSysCallback

		for cbname in self.nbrain.system_callbacks:

			if cbname not in 'onUserCreate onCreate'.split():

				nuke_real_callback = getattr( nuke, 'add' + cbname[0].upper() + cbname[1:], None)
				nuke_real_remove_callback = getattr(nuke, 'remove' + cbname[0].upper() + cbname[1:], None)

				if nuke_real_callback and nuke_real_remove_callback:

					args = ( self.nbrain.name , cbname  ) 

					nuke_real_callback( trigger , args = args , nodeClass = 'PanelNode' )

					self.nbrain.applied_callbacks.append(  ( trigger , args , nuke_real_remove_callback )  )






	def apply_onKnobCallback_callback( self ):
		
		def onKnobCallback( panel_id ):

			this = space.this()
					
			nbrain = brain.nodeScript.byPanel[ panel_id ]
			
			this.PANEL = self
			
			this.DIALOG , node , this.WIDGET = nbrain.dynamic_bundle # extra info

			if this.KNOBS( 'panel_id' , None , create_att = False ) and this.VALUES.panel_id == node.knobs()['panel_id'].value():
				
				if brain( 'AUTO_REFRESH_NODE' , False ):
									
					self.refresh_panel()
				
				callbacks = nbrain.knob_callbacks.get( this.KNOB.name() , [] )

				#print 'DEBUG: ' , this.KNOB.name() , callbacks
	
				for callback in callbacks:

					callback( this )



		args = ( self.nbrain.name , ) # panel id

		trigger = onKnobCallback  #brain.Lib.nodes3_triggers.userCallbacks_Trigger

		nuke.addKnobChanged( trigger , args , nodeClass = 'PanelNode' )	

		self.nbrain.applied_callbacks.append(  ( trigger , args , nuke.removeKnobChanged )  )

		#print '\t'*2 , 'added "GLOBAL knobChanged" on %s node class' % node_class



	
		
















