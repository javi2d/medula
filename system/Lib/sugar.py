





# with statements


class open_shelve:
	
	def __init__( self ,  path):
	
		self.path = path
	
	def __enter__( self  ):
		
		import shelve
		
		self.db = shelve.open( path ,'wb' )
		
		return self.db
		
	def __exit__( self ):
		
		 self.db.close()
		


# decorators
		

class nuke_thread:

	def __init__( self , function ):

		self.function = function
	
	def __call__( self , *args , **kwargs ):
		
		self.args = args
		
		self.kwargs = kwargs
		
		def nuke_wrapper( self ):
		
			nuke.executeInMainThread( self.function , self.args , self.kwargs )
		
		thread = sop.Core.thread( nuke_wrapper , self )
		
		print '@ nuke_thread about to run nuke.execute....'
		
		nuke.executeInMainThread( thread.start )
        
		return thread

