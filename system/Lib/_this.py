

#import nuke
import socket

class this(object):
	
	__counter__ = 0
	
	__ext__ = Brain()
	
	
	def __init__(self , NODE = None , KNOB = None ):
		
		self._NODE = NODE
		self._KNOB = KNOB
		
		
		# for debug purposes
		
		this.__counter__ += 1
	
	
	
	def __call__(self , NODE = None , KNOB = None ):
		
		if NODE or KNOB:
			
			new_this = this( NODE = NODE , KNOB = KNOB )
			
			return new_this
			
		else:
		
			self._NODE = NODE 
			self._KNOB = KNOB 

			return self
	
	
		
	def __lshift__( self , other ):
		
		if type( other ).__name__ == 'Space':
			
			if not other['called'] : other = other['exec']
			
			for k,v in other['user_logic'].items():
				
				setattr( this.__ext__ , k , v )
				
	
			
	def __getattr__(self, att):
		
		return self.__common_getattr__( self , att )
		

		
	@staticmethod
	def __common_getattr__( self , att ):
		
		'''
		
		
		
		'''
		
		if att in this.__ext__['names']:
			
			return this.__ext__( att )( self )
		
		
		# CUSTOM EXTENSION CONFIG , OVERRIDES DEFAULT
		######################################################		
		# NODES AND KNOBS
		
		
		
		
		elif att == 'ROOT':
			
			try:
			
				new_this = this( nuke.Root() )
				return new_this
				
			except:
				
				raise RuntimeError( '\nRoot node cannot be resolved at this time.\n')	
		
		
		elif att == 'ROOT_NODE':
			
			return nuke.Root()
			
		
				
		
		elif att == 'NODE':
			
			node = ( self._NODE or nuke.thisNode() ) 
				
			return node

		
		elif att == 'SAFE_NODE':
			
			node = nuke.thisNode()
			
			try:
        
				node.knobs()
				
				return node #self.NODE
        
			except:
        
				return None
		
		elif att == 'TYPE':
			
			return type( self.NODE ).__name__
		
		
		elif att == 'CLASS':
			
			if self.TYPE == 'PanelNode':
	
				return self.VALUES( 'panel_id' , 'Panel' , create_att = False )
				
			else:
	
				return self.NODE.Class()     # ( self._NODE or nuke.thisNode()  ).Class()  # or nuke.Root()
		
					
		elif att == 'KNOB':
			
			return  ( self._KNOB or nuke.thisKnob() )
		
		
		
		elif att == 'SAFE_KNOB':
        
			if self.SAFE_NODE:
        
				return self.KNOB
		
			
			
		
		elif att == 'VALUE':
			
			knob =  self.KNOB
			
			if knob:
				
				return knob.value()
		
			
		elif att == 'KNOBS':
			
			node = self.NODE
			
			if node:
			
				KNOBS = Brain()
				
				for knob_name , knb in node.knobs().items():
					
					setattr( KNOBS, knob_name, knb )
				
				return KNOBS['lock']
		
				
		elif att == 'SORTED_KNOBS':
			
			node = self.NODE
			
			if type( node ).__name__ == 'PanelNode':
				
				knobs = [ self.KNOBS( k.name() ) for k in self.PANEL_NBRAIN.knobs if k not in '[ ]'.split() and k.name() in self.KNOBS['names']]
				
				return knobs

			elif hasattr( node , 'allKnobs' ):
				
				return node.allKnobs()
			
			else:
				
				return [ node.knob(i) for i in range( node.getNumKnobs() ) ]
		
			
		elif att == 'SORTED_VALUES':
			
			node = self.NODE
			
			return [ node.knob(i).value() for i in range( node.getNumKnobs() ) ]			
		
		
		elif att == 'SORTED_NAMES':
			
			return self.NODE.writeKnobs( nuke.WRITE_ALL ).split()
			
			
			#node = self.NODE  #( self._NODE or nuke.thisNode() )
			#return [ node.knob(i).name() for i in range( node.getNumKnobs() ) ]
		
		
		elif att == 'SORTED_ITEMS': # ( name , value )
			
			node = self.NODE  #( self._NODE or nuke.thisNode() )
			
			return [ ( node.knob(i).name() , node.knob(i).value() ) for i in range( node.getNumKnobs() ) ]
		
		
		elif att == 'SORTED_TOSCRIPT_ITEMS': # ( name , toScript )
			
			node = self.NODE  #( self._NODE or nuke.thisNode() )
			
			return [ ( node.knob(i).name() , node.knob(i).toScript( True , context = None ) ) for i in range( node.getNumKnobs() ) ]
		
		
		elif att == 'VALUES':
			
			node = self.NODE  
			
			if node:
			
				VALUES = Brain()
				
				for knob_name , knb in node.knobs().items():
					
					setattr( VALUES, knob_name, knb.value() )
			
				return VALUES['lock']
		
		
		elif att == 'BRAIN':
			
			NODE = self.NODE  # ( self._NODE or nuke.thisNode() )
			
			if isinstance( NODE, nuke.PanelNode ):
				
				return main.brain('DATA.PANELS.%s' % NODE.knobs()['panel_id'].value().replace('.','_') , Brain() )
			
			else:
				
				return main.brain('DATA.NODES.%s' % NODE.Class() , Brain() )
		
				
		elif att == 'NODES':
			
			Node = self.NODE  #( self._NODE or nuke.thisNode() )
			
			NODES = Brain()
			
			if isinstance( Node, nuke.Group ):
				
				allNodes = Node.nodes()
			
			else:
				
				allNodes = nuke.allNodes()
					
			for node in allNodes:
					
				NODES( node.name() , node )
						
			return NODES['lock']
		
		
		elif att == 'THIS_NODES': # same as nodes but in 'this' format
			
			Node = self.NODE  # ( self._NODE or nuke.thisNode() )
			
			NODES = Brain()
			
			if isinstance( Node, nuke.Group ):
				
				allNodes = Node.nodes()
			
			else:
				
				allNodes = nuke.allNodes()
					
			for node in allNodes:
					
				NODES( node.name() , this( node ) )
						
			return NODES['lock']
			
		
		elif att == 'ALL_NODES':
			
			return nuke.allNodes()
		
		
		elif att == 'ALL_THIS_NODES':
			
			return [ this( n ) for n in nuke.allNodes() ]
		
		
		
		elif att == 'SELECTED_NODE':
			
			try:
				
				return this( nuke.selectedNode() )
			
			except ValueError:
				
				return  None #this( nuke.Root() )
		
		
		elif att == 'ROOT_SELECTED_NODE':
			
			nuke.Root().begin()
			
			selected_in_root = self.SELECTED_NODE
			
			nuke.Root().end()
			
			return selected_in_root
			
		
		
		elif att == 'SELECTED_NODES':
			
			return [ this( n ) for n in  nuke.selectedNodes() ]
		
		
		elif att == 'ROOT_SELECTED_NODES':
			
			
			nuke.Root().begin()
			
			return self.SELECTED_NODES
			
			nuke.Root().end()
		
		
		
		elif att == 'NODES_BY_CLASS':

			Node = self.NODE  # ( self._NODE or nuke.thisNode() )
			
			NODES = Brain()
			
			if isinstance( Node, nuke.Group ):
				
				allNodes = Node.nodes()
			
			else:
				
				allNodes = nuke.allNodes()

			for node in allNodes:
				
				current_class_list = NODES( node.Class() , [] )
				current_class_list.append( node )

			return NODES['lock']
		
		
		elif att == 'PARENT':
			
			parent = nuke.thisParent() 
			
			if not parent:
				
				parent = nuke.Root()
			
			return parent
		
		
		# NODES AND KNOBS
		######################################################		
		# NETWORK		

		
			
		elif att == 'HOSTNAME':
			
			return socket.gethostname().split('.')[0]
			
			
		elif att == 'HOSTLABEL':
			
			hostlabel = ''
			
			for char in self.HOSTNAME:
				
				hostlabel += ( char if char.isalnum() else '_' )					
			
			return hostlabel
		
		
		elif att == 'LOGIN':

			return os.path.basename( os.path.expandvars( '$HOME' ) )


		elif att == 'USER':

			return self.LOGIN
		
		
		
		elif att == 'USER_ID':
			
			return '%s_%s' % ( self.HOSTLABEL , self.USER )
		
		
		
		elif att == 'HOME':
			
			return os.path.expandvars( '$HOME' )
			
		
		
		elif att == 'OPERATOR':
			
			return brain.Sources( '%s._operator' % self.HOSTLABEL , self.HOSTLABEL )
			


		# NETWORK
		######################################################		
		# NBRAIN	


		#elif att == 'NBRAIN':
			
		#	return  self.PANEL_NBRAIN or self.NODE_NBRAIN or self.CLASS_NBRAIN
		
		
		elif att == 'PANEL_NBRAIN':

			byPanel = brain.nodeScript( 'byPanel' , {} )
			
			panel_id = self.VALUES( 'panel_id' , None )
			
			if panel_id and panel_id in byPanel:

				return byPanel[ panel_id ]
		
		
		elif att == 'NODE_NBRAIN':

			byNode  = brain.nodeScript( 'byNode' , {} )

			userNode_id = self.VALUES( 'userNode_id' , None )
			
			print 'this.NODE_BRAIN >>>' , userNode_id , byNode.keys()
			
			if userNode_id and userNode_id in byNode:

				return byNode[ userNode_id ]
		
		
		
		elif att == 'CLASS_NBRAIN':
			
			byClass = brain.nodeScript( 'byClass' , {} )
			
			if self.CLASS in byClass:
				
				return byClass[ self.CLASS ]
		

		#elif att == 'SPACE':
		#	
		#	return self.NBRAIN.space
		
		
		# NBRAIN
		######################################################		
		# SCRIPT




		elif att == 'SCRIPT_PATH':
			
			tcl_value = nuke.tcl( 'value root.name' )
			
			if tcl_value:
				
				return Normalize.path( tcl_value )
				
			else:
				
				return ''
		
		
		elif att == 'SCRIPT_NAME':
			
			if self.SCRIPT_PATH:
				
				return os.path.splitext( os.path.basename( self.SCRIPT_PATH ) )[0]
			
		
		
		elif att == 'SCRIPT_FOLDER':
			
			if self.SCRIPT_PATH:
	
				return Normalize.dirname( self.SCRIPT_PATH )



sop.Expose.object( this() , 'this' )






	
