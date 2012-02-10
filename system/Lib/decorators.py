
#class executeThreadWithResult:
#	
#	def __init__( self , function ):
#	
#		self.function = function
#	
#	def __call__( self , *args , **kwargs ):
#		
#		self.args = args
#		
#		self.kwargs = kwargs
#		
#		#def thread_wrapper( self ):
#			
#		thread = sop.Core.thread( self.function , *self.args, **self.kwargs )
#			
#		thread.start()
#			
#		#nuke.executeInMainThread( thread_wrapper , ( self , ) )



class executeInMainThread:
	
	def __init__( self , function ):
	
		self.function = function
	
	def __call__( self , *args , **kwargs ):
		
		self.args = args
		
		self.kwargs = kwargs
		
		def nuke_wrapper( self ):
		
			nuke.executeInMainThread( self.function , self.args , self.kwargs )
		
		thread = sop.Core.thread( nuke_wrapper , self )

		thread.start()

		return thread
	
	
class executeInMainThreadWithResult:

	def __init__( self , function ):
	
		self.function = function
	
	def __call__( self , *args , **kwargs ):
		

		self.args = args
		
		self.kwargs = kwargs
		
		def nuke_wrapper( self ):
				
			nuke.executeInMainThreadWithResult( self.function , self.args , self.kwargs )
		
		thread = sop.Core.thread( nuke_wrapper , self )
		
		thread.start()
		
		return thread