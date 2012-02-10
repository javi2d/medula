
import sqlite3	



'''
__root__

name    |  value
----------------
'var'   |  100
		|
'table' |  NULL





'''




class Table( object ):
		
	def __init__( self , name , parent  ):

		self.__name__ = name
		self.__parent__ = parent
 		
		con = self['con']
		
		table_name = '"%s"' % self['route']
		
		print 'DEBUG creating table : %s ' % table_name
		
		con.CREATE(  table_name , 'name TEXT UNIQUE , value TEXT '  )
	
	
	def __con__( self ):
	
		parent = self

		while 1:

			parent = parent.__parent__

			if type( parent ).__name__ == 'Connection':

				return parent

			elif type( parent ).__name__ == 'Table':

				continue

			else:

				raise RuntimeError, 'cursor cannot be reached'
	
	def __route__( self ):
		
		# compute route of table

		route = [ ]

		parent = self

		while hasattr( parent , '__name__' ) and hasattr( parent , '__parent__' ):

			route.append( parent.__name__ )

			parent = parent.__parent__

		return '.'.join( route[:-1][::-1] )

		
		
	def __getitem__( self , query ):

		if False : pass

		elif query == 'con':
			
			return self.__con__()
	
		elif query == 'route':
			
			return self.__route__()

			
	
	
	def __setattr__( self , att , value ):
		
		if  att.startswith( '__' ) and att.endswith( '__' ):
		
			object.__setattr__( self , att , value)
		
		else:
			
			# value transformation and store in the database
			
			con = self['con']
			
			print 'Added row in con: %s route: %s' % (  con , self['route'] ) 
			
			print '     att: %s value: %s ' % ( att , repr( value ) )
			
			
			
			
			
		
	def __getattr__( self , att ):
		

		return Table( att , self )


	def __dir__( self ):

		return self['con'].TABLES()










class Connection( object ):
	
	QUEUE = []
	
	DEBUG = False
		
	def __new__( cls , database  ):

		self = super( Connection, cls ).__new__(cls)

		self.DATABASE = sop.Normalize.path( database )

		return Table( '__root__' , self )	
	

	def __getattr__( self , att ):
		
		if att == 'CONNECTION':
			
			con = sqlite3.connect( self.DATABASE , timeout = 15	 ) #, isolation_level = None
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
		
		sql = "SELECT %s FROM %s %s" % ( names , table , expr )
		
		print '\nDEBUG SELECT:' , sql 
		
		cur = self.EXECUTE( sql )
		
		return cur.fetchall()

	
	
	
	def TABLE_INFO( self, table ):
				
		cur = self.EXECUTE( 'PRAGMA table_info( %s )' % table )
		
		return cur.fetchall()
	
	
	
	def COLUMNS( self , table ):
			
		return [ x[1] for x in self.TABLE_INFO( table ) ]
	

	def TABLES( self ):
		
		cur = self.EXECUTE( "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name" )	
		return [ str( x[0] ) for x in cur.fetchall() if	 not x == ( u'sqlite_sequence', ) ] 
		

	def SCHEMA( self ):
		
		cur = self.EXECUTE( "SELECT * FROM sqlite_master"  )		
		return cur.fetchall()
		
	
	def TABLE_SCHEMA( self ):
		
		return [ s for s in self.SCHEMA() if s[0] == 'table' ]
	
	
	def ALTER_TABLE( self , table , expr , execute = True ):
		
		sql = 'ALTER TABLE %s %s' % ( table, expr )
		
		self.QUEUE.append( ( sql , None ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		
		
	def INSERT( self , query , values ,	 execute = True ):
		
		params = ','.join(	' ?' for i in range( len( values ) )  ) 
		
		sql = 'INSERT OR REPLACE INTO %s VALUES ( %s )' % ( query , params ) 
		
		print '\nDEBUG INSERT:' , sql , values
		
		self.QUEUE.append( ( sql , values ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		#return self.EXECUTE_QUEUE()	
	
	def UPDATE( self , table , names , expr	 , values  ,  execute = True ):
		
		names = ','.join(  '%s = ?' % n.strip() for n in names.split(',')  ) 
		
		sql = 'UPDATE %s SET %s %s' % ( table , names , expr ) 
		
		print '\nDEBUG UPDATE:' , sql , values
		
		self.QUEUE.append( ( sql , values ) )
		
		if execute: return self.EXECUTE_QUEUE()
		
		
	
	def EXECUTE( self , sql = None , params = None	):
		
		if not sql:
			
			return self.EXECUTE_QUEUE()
		
		else:
			
			self.QUEUE.append( ( sql , params )	 )	
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









class Cursor( object ):


	def __new__( cls , database  ):
		
		self = super(Cursor, cls).__new__(cls)
		
		self.__db__ = sop.Normalize.path( database )
		
		return Table( '__root__' , self ) 
	
	
	def __init__( self , database ):
		
		self.__db__ = sop.Normalize.path( database )
		

	def __dir__( self ):
		
		return self['connection'].TABLES()
	
	def __getattr__( self , att ):
		
		print '#01 ' , att
		
		return Table( att , self )
	
	def __setattr__( self , att , value ):
    
		if  att.startswith( '__' ) and att.endswith( '__' ):
    
			object.__setattr__( self , att , value)
    
		else:
			
			# Create new table
			
			print 'WARNING : Forbidden setattr on Cursor' , att , value
	
		
	def __getitem__( self , query ):
		
		if False : pass
		
		elif query == 'connection':

			return	Connection( self.__db__ )
	
		








'''

class Cursor2( object ):

	
	def __init__( self , database , table = '__root__' ):

		self.__db__ = sop.Normalize.path( database )
		
		self.__table__ = table
		
		if self.__table__ not in self['tables']:

			self.__root__()
	

	def __root__( self , clear = False ):
		
		con = self[ 'connection' ]
		
		
		if clear:
			
			con.CLEAR()
		
		
		con.CREATE( self.__table__ , '__meta__ TEXT UNIQUE' )
		
		for metaname in 'value cdate mdate'.split():
		
			con.INSERT( '%s( __meta__ )' % self.__table__ , ( metaname ,  )   )
		


	def __reset__( self ):
		
		self.__root__( clear = True )
		
	
	
	def __str__( self ):
		
		print self['table']
		
		print self['names']
		
		print self['connection']
		
		return ''
		
		

	def __getitem__( self , query ):
		
		if query == 'table':
			
			return self.__table__
		
		
		elif query == 'tables':

			return self['connection'].TABLES()
			
		elif query == 'values':
			
			#print '******' , ','.join( self['names'] )
			
			return self['connection'].SELECT( ','.join( self['columns'] ) , self['table']  ) #, 'WHERE __meta__ = "value"'
			
		
			
		elif query == 'columns':
			
			return self['connection'].COLUMNS( self['table'] )
			
		
		elif query == 'reset':
			
			# enforces to call the query
			
			return self.__reset__
		
	
		elif query == 'names':
			
			return [ x for x in self['columns'] if not x.startswith('__') ]
		
		elif query == 'connection':
			
			return	Connection( self.__db__ )
	
		
	def __call__( self ):
		
		raise 
	
	def __dir__( self ):
		
		db = Connection( self.__db__ )
		
		print 1
		
		return db.COLUMNS( self['table'] )
		
		
	def __getattr__( self , att ):
		
		db = Connection( self.__db__ )
		
		if att in db.COLUMNS( self['table'] ):
			
			value = db.SELECT( att , self['table'] , 'WHERE __meta__ = "value"' )
			
			if value:
			
				value = value[0][0]
			
				try:
				
					return eval(  value )
				
				except:
				
					return value
					
			else:
				
				print 'WARNING,  NO VALUE att = %s , table = %s' % ( att, self['table'] )
				
				
				#return sop.Void
				

		else:
			
			print 'Autocreated intermediate database.Cursor'
			
			return Cursor( self.__db__ , att )
			
			#raise AttributeError , 'att [ %s ] not in database. This should create a new table named as "att"' % att
		
	
	
	def __setattr__( self , att , value ):
		
	
		
		if	att.startswith( '__' ) and att.endswith( '__' ):
			
			object.__setattr__( self , att , value)
			
		else:
			
			
			#if type( value ).__name__ in [ 'str' , 'unicode' ]:

			value = repr( value )  #"'%s'" % value
		
			db = Connection( self.__db__ )
			
			if att not in db.COLUMNS( self['table'] ):
				
				db.ALTER_TABLE( self['table'] , 'ADD COLUMN %s TEXT' % att	)
			
			db.UPDATE( self['table'] , att , 'WHERE __meta__ = "value"', ( value , )	)
			
			



'''




