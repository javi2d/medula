


class open_shelve:
	
	def __init__( self ,  path):
	
		self.path = path
	
	def __enter__( self  ):
		
		import shelve
		
		self.db = shelve.open( path ,'wb' )
		
		return self.db
		
	def __exit__( self ):
		
		 self.db.close()
		
		
		
		
		
		