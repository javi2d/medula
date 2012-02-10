

		
#class plaintextSolver( sop.Solver ):
#	
#	tag = 'plaintext'
#	targets = [ '.txt' ]
#	
#	def __solve__(self):
#		
#		f = open(self.path)
#		text = f.readlines()
#		f.close()
#		
#		self.space.__PLAINTEXT__ = text
#
#plaintextSolver()





class pythonSolver( sop.Solver ):

	tag = 'python/marshal'

	targets = [ '.py', '.pyc', '.pyo', '.marshal' ]

	def __solve__(self):
		
		sop.Core.execution( self.path , self.space)
		
pythonSolver()






class knobsSolver( sop.Solver ):

	tag = 'knobs'
	targets = [ '.knobs'  ]

	def __solve__(self):
		
		knobs_space = sop.sh( self.path )

		knobs_space << brain.Lib.knobs

		knobs_space.__proto__ = sorted( knobs_space.__dict__.copy().items() )
		
		self.space << knobs_space['exec']
		


knobsSolver()




class userNodeSolver( sop.Solver ):
	
	tag = 'userNode'
	targets = ['.userNode','.uNode']
	
	def __solve__(self):
		
		brain.Lib.userNodes5.solve( self.path )

userNodeSolver()



		
class nodeSolver( sop.Solver ):
	
	tag = 'node'
	targets = ['.node']
	
	def __solve__(self):
		
		self.space.__NBRAIN__ = brain.Lib.nodes7.solve( self.path )


nodeSolver() 






	
class panelSolver( sop.Solver ):

	tag = 'panel'
	targets = [ '.panel' , '.mpanel' ]

	def __solve__(self):
			
		panel =  brain.Lib.panel3.Dynamic_Panel( self.path )
		
		if self.ext in ['.panel']:
		
			panel.show()
		
		else:
			
			panel.showModal()

panelSolver()		






class templateSolver( sop.Solver ):
	
	tag = 'template'
	targets = ['.nk']
	
	def __solve__(self):
		
		group = nuke.createNode('Group')
		
		def create_nodes():
			
			nuke.scriptReadFile(self.path)
		
		try:
			
			group.run( create_nodes )
		
			self.space.__TEMPLATE__ = group.nodes()
		
		except RuntimeError, e:
			
			nuke.message( 'Version mismatch, template may not work in current nuke version.\n\nTraceback: %s' % e )
			
		finally:
		
			group.expand()

templateSolver() 			






class gizmoSolver( sop.Solver ):
	
	tag = 'gizmo'
	targets = [ '.gizmo' ]
	
	def __solve__(self):
				
		nuke.pluginAddPath( self.dirname )
			
		try:
			self.space.__GIZMO__ = nuke.createNode( self.name + self.ext )
			self.space.__GIZMO__.setName(self.name)
		
		except:
			
			#print 'Gizmo [ %s ] cannot be loaded, hard reload nuke to make it available.' % self.name + self.ext
			
			raise
			
gizmoSolver() 



		
class commandSolver( sop.Solver ):

	tag = 'cmd'
	targets = [ '.cmd' ]

	def __solve__(self):

		sop.Core.execution( self.path , self.space)

commandSolver()














		
		