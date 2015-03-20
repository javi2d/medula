

import os
import sys
import mdl

HOSTNAME = mdl.net.hostname()

DEFAULTS = {
'username': '',
'hostname': '',
'ip'      : '',
'local'   : '',
'remote'  : '',
'isref'   : False
}

def __call__( self , path ):

	path = mdl.shell( path , delegated = 1 )
	return __mod__.Sources( path )


__mod__ = mdl.uber.uberModule()


class Sources( dict ):

	'Relaciones de los paths'

	__metaclass__ = mdl.uber.uberClass

	def __init__( self , path ):

		self.path = mdl.shell( path , delegated = 1 )
		self.ds   = mdl.data.DataSpace( self.path )

		if not __mod__.HOSTNAME in self.ds:
			with self.ds:
				item = self.ds[ __mod__.HOSTNAME ] = __mod__.DEFAULTS.copy()
				item['username'] = mdl.shell( '$HOME' ).BASENAME
				item['hostname'] = mdl.net.hostname( normalize = False )

		self.references = []
		self.load()

	def __getitem__( self , key ):

		if key == 'localhost':
			key = __mod__.HOSTNAME

		return super( type(self) ,self ).__getitem__( key )

	
	def dump( self ):

		result = {}

		for key,item in self.iteritems():
			result.setdefault( key , {} )
			for k in __mod__.DEFAULTS:
				value = item[k]
				if isinstance( value , list ):
					value = '; '.join( value ) 
				result[key][k] = value

		with self.ds:
			self.ds.clear()
			self.ds.update( result )


	def load( self ):

		'inicializamos el archivo si localhost esta no definido'
		
		def norm_paths( key , item ):

			if isinstance( item[ key ] , (str,unicode) ):
				item[ key ] = [ p.strip() for p in item[ key ].split(';') if p.strip() ]
			item[ key ] = [ mdl.shell(p) for p in item[key] ] 
			assert isinstance( item[ key ] , list )


		self.ds.load()
		self.clear()
		self.update( self.ds )

		self.references = []

		for key,item in self.iteritems():

			norm_paths( 'local' ,item )
			norm_paths( 'remote' ,item )

			if key == __mod__.HOSTNAME:
				item['paths'] = item['local'] + item['remote'] 	
			else:
				item['paths'] = item['remote']

			item['alive'] = None

			for p in item['paths']:
				p = mdl.shell(p)
				if p.EXISTS:
					item['alive'] = p
					os.environ[key] = p
					break

			if item['alive']:
				if key == __mod__.HOSTNAME or item['isref']:
					self.references.append( item['alive'] )

		mdl.log.info( 'rebuild [hosts] = %s' % self.keys() )

	def alive( self , key ):

		if key in self:
			return self[key]['alive']

	def sorted_keys(self):

		sort = lambda k : 0 if k == __mod__.HOSTNAME else k
		keys = super( type(self),self ).keys()
		return sorted( keys , key = sort )		

	def sorted_items( self ):

		return [ (k,self[k]) for k in self.sorted_keys() ]


	def add_resource( self, name ):

		'Crea un nuevo recurso con nombre -name- y reconstruye SOURCES'

		self.load()
		item = self.setdefault( name , __mod__.DEFAULTS.copy() )
		#item['hostname'] = mdl.net.hostname( normalize = False )
		self.dump()


	def add_path( self, key , path ):

		'Annade el path al key'

		path = mdl.shell( path , delegated = 1 )
		
		self.load()

		assert key in self, 'El recurso "%s" no esta registrado en sources.' % key

		item = self[ key ]

		path_key = 'local' if key == __mod__.HOSTNAME else 'remote'
		
		target = item[ path_key ]

		if path not in target:
			target.append( path )

		self.dump()



	'Sources related functions'

	'MIRAR QUE OCURRE SI HAY DOUBLE MATCHES O VARIOS RECURSOS EN EL MISMO HOST'

	def local_key( self ):
		return mdl.net.hostname()


	def local_item( self ):
		return self[ self.local_key() ]



	'Mirar donde se utiliza esto por que ahora ya no es siempre resultado'

	def local_root( self ):
		return self.local_item()['alive'] #or mdl.shell( '$HOME' )


	def key_root( self , key ):	
		return self[key]['alive']


	def path_key( self , path ):

		'Da el key en el que esta definido path'

		path = mdl.shell( path , delegated = 1 )

		for key,item in self.sorted_items():
			for p in item['paths']:
				if path == p or path.startswith( p ):
					return key

	'Hay que asumir que todo el material esta relinkado y por tanto solo tienen validez los paths relativos al host actual'

	def path_root( self , path ):

		path = mdl.shell( path , delegated = 1 )

		for key,item in self.sorted_items():
			for p in item['paths']:
				if path == p or path.startswith( p ):
					return p

	def path_tail( self , path ):

		path = mdl.shell( path , delegated = 1 )
		root = self.path_root( path )	
		return path.relpath( root )




	def path_relink( self , path , owner ):

	
		'RELINK PATH'
		path = mdl.shell( path , delegated = 1 )

		if owner == mdl.net.hostname() and path.DIRNAME.EXISTS:
			return path

		'Tenemos un path que no existe y un sitio donde puede que exista'

		'Lista de doble itmes ( search, replace )'
		matches = []

		#print 'Testing' , path 

		for key,item in self.sorted_items():
			alive = item['alive']
			if alive:
				paths = item['remote']
				if key==owner:
					'Tener en cuenta el local'
					paths = item['local'] + paths

				for p in paths:

					#print '->' , key , owner , item['local'] , p+'/'

					if ( path+'/' ).startswith( p+'/' ):
						matches.append( (p,alive) )


		#print 'DEBUG Matches' , path
		#print '     ' , matches

		if len(matches) == 1:
			'Esto deberia ser lo normal'

			srch,rep = matches.pop()
			'Ya sabemos que esta vivo el recurso'
			path_result = path.replace( srch , rep , 1 )
			return path_result


		elif len(matches) > 1:
			'Esto es extraordinario y da pie a malinterpretaciones'
			raise RuntimeError, 'Incoherencia con paths %s' % matches
		else:
			'Cero matches , do NOTHING'








