



class Cursor( object ):
	
	def __init__( self , database , table = '__root__' ):

		self.__db__ = Normalize.path( database )
		
		self.__table__ = table
		
		con = self[ 'connection' ]
		
		con.CREATE( self.__table__ , '__type__ TEXT UNIQUE' )
		
		con.INSERT( '%s( __type__ )' % self.__table__ , ( 'value' , )  )
		
		



	def __getitem__( self , query ):
		
		if query == 'table':
			
			return self.__table__
		
		elif query == 'names':
			
			return [ x for x in self['connection'].COLUMNS( self['table'] ) if not x.startswith('__') ]
		
		elif query == 'connection':
			
			return 	Connection( self.__db__ )
	
		
	def __call__( self ):
		
		raise 
	
	def __dir__( self ):
		
		db = Connection( self.__db__ )
		
		print 1
		
		return db.COLUMNS( self['table'] )
		
		
	def __getattr__( self , att ):
		
		db = Connection( self.__db__ )
		
		if att in db.COLUMNS( self['table'] ):
			
			value = db.SELECT( att , self['table'] , 'WHERE __type__ = "value"' )[0][0]
			
			try:
				
				return eval(  value )
				
			except:
				
				return value
				

		else:
			
			return Cursor( self.__db__ , att )
			
			#raise AttributeError , 'att [ %s ] not in database.' % att
		
	
	
	def __setattr__( self , att , value ):
		
	
		
		if  att.startswith( '__' ) and att.endswith( '__' ):
			
			object.__setattr__( self , att , value)
			
		else:
			
			
			if type( value ).__name__ in [ 'str' , 'unicode' ]:

				value = repr( value )  #"'%s'" % value
			
			
			db = Connection( self.__db__ )
			
			if att not in db.COLUMNS( self['table'] ):
				
				db.ALTER_TABLE( self['table'] , 'ADD COLUMN %s TEXT' % att  )
			
			#print 'INSERT '
			
			#db.EXECUTE( '' )
			
			#db.UPDATE( '__root__( __type__ , %s )' % att , ( 'value' , value  ) )
			
			db.UPDATE( self['table'] , att , 'WHERE __type__ = ?', ( value , 'value' )  )
			
			







import sqlite3	

class Connection( object ):
	
	QUEUE = []
	
	DEBUG = False
	
	def __init__( self , database ):
			
		self.__database__ = database
	
	
	def __getattr__( self , att ):
		
		if att == 'BRAIN':
			
			return Brain( self.__database__ )
		
		elif att == 'CONNECTION':
			
			con = sqlite3.connect( self.__database__ , timeout = 15  ) #, isolation_level = None
			con.commit()

			return con
	
	
	def CLEAR( self , execute = True ):
		
		all_tables = ','.join( self.TABLES() )		
		self.DROP( all_tables , execute = execute )
		
		
	def DROP( self, tables , execute = True ):

		if tables == '*':
			
			tables = self.TABLES()
		
		else:

			tables = [ t.strip() for t in tables.split(',') ]
	
		
		for table in tables:
		
			self.QUEUE.append( ( 'DROP TABLE IF EXISTS %s' % table, None ) )
	
		
		if execute: return self.EXECUTE_QUEUE()
	
	
		
	def SELECT_ALL( self, table , expr = '' ):	
		
		cur = self.EXECUTE( "SELECT * FROM %s %s" % (  table , expr ) )
		
		return cur.fetchall()
	
	
	def SELECT( self , names , table , expr = ''  ):
		
		cur = self.EXECUTE( "SELECT %s FROM %s %s" % ( names , table , expr ) )
		
		return cur.fetchall()

	
	
	
	def TABLE_INFO( self, table ):
				
		cur = self.EXECUTE( 'PRAGMA table_info( %s )' % table )
		
		return cur.fetchall()
	
	
	
	def COLUMNS( self , table ):
			
		return [ x[1] for x in self.TABLE_INFO( table ) ]
	

	def TABLES( self ):
		
		cur = self.EXECUTE( "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name" )	
		return [ str( x[0] ) for x in cur.fetchall() if  not x == ( u'sqlite_sequence', ) ]	
		

	def SCHEMA( self ):
		
		cur = self.EXECUTE( "SELECT * FROM sqlite_master"  )		
		return cur.fetchall()
		
	
	def TABLE_SCHEMA( self ):
		
		return [ s for s in self.SCHEMA() if s[0] == 'table' ]
	
	
	def ALTER_TABLE( self , table , expr , execute = True ):
		
		sql = 'ALTER TABLE %s %s' % ( table, expr )
		
		self.QUEUE.append( ( sql , None ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		
		
	def INSERT( self , query , values ,  execute = True ):
 		
		params = ','.join(  ' ?' for i in range( len( values ) )  ) 
		
		sql = 'INSERT OR REPLACE INTO %s VALUES ( %s )' % ( query , params ) 
	
		self.QUEUE.append( ( sql , values ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		#return self.EXECUTE_QUEUE()	
	
	def UPDATE( self , table , names , expr  , values  ,  execute = True ):
		
		names = ','.join(  '%s = ?' % n.strip() for n in names.split(',')  ) 
		
		sql = 'UPDATE %s SET %s %s' % ( table , names , expr ) 
		
		#print 'DEBUG UPDATE:' , sql , values
		
		self.QUEUE.append( ( sql , values ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		
	
	def EXECUTE( self , sql = None , params = None  ):
		
		if not sql:
			
			return self.EXECUTE_QUEUE()
		
		else:
			
			self.QUEUE.append( ( sql , params )  )	
			return self.EXECUTE_QUEUE()	
	
	
	
	def EXECUTE_QUEUE( self ):
		
		try:
		
			with self.CONNECTION as con:	

				cur = con.cursor()

				for sql, params in self.QUEUE:
				
					if self.DEBUG : print 'sql $ ( params : %s ) %s ' % ( params , sql )

					if params: 
						cur.execute( sql , params )
					
					else: 
						cur.execute( sql )
			
				
			con.commit()
			
				
		except:
			
			#if con:
		    #    
			#	con.rollback()

		    raise

		
		finally:
			
			self.QUEUE[:] = []
			return cur
	
	
	def CREATE( self, tables , schema , replace = False , execute = True ):

		tables = [ t.strip() for t in tables.split(',') ]

		for table in tables:

			if replace:

				self.QUEUE.append( ( 'DROP TABLE IF EXISTS %s' % table , None ) )

			self.QUEUE.append( ( 'CREATE TABLE IF NOT EXISTS %s( %s )' % ( table, schema ) , None ) )

		if execute: return self.EXECUTE_QUEUE()


