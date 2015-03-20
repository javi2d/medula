
"""
.. module:: shell
.. moduleauthor:: Javier Garcia <javi2d@invalid.com>
"""



import sys
import os
import inspect
import types
from contextlib import contextmanager
import StringIO
import imp
import marshal
import re
import glob
import time
import filecmp
import shutil
import random
import logging
import tempfile


TEMP_FILES = {} 


def __call__( self , route , **kwargs ):

	kwargs['delegated'] = kwargs.setdefault( 'delegated' , 0 ) + 1
	return __mod__.Shell( route , **kwargs )

import mdl
__mod__ = mdl.uber.uberModule()


 ######  ##     ## ######## ##       ##       
##    ## ##     ## ##       ##       ##       
##       ##     ## ##       ##       ##       
 ######  ######### ######   ##       ##       
      ## ##     ## ##       ##       ##       
##    ## ##     ## ##       ##       ##       
 ######  ##     ## ######## ######## ######## 


os.environ.setdefault( 'HOME' , os.path.expanduser('~') )

#@mdl.uber.uberCallable
class Shell( str ):

	def __call__( self , relative ):

		path = __mod__.join( self , relative )
		return type( self )( path )


	def __new__( cls , route , delegated = 0 , absolute = False ): #, stack_offset = 0 , stack = None , , stack = None

		assert isinstance( route , str ), 'First arg should be path string, current is : (%s) "%s"' % ( type(route).__name__,repr(route) ) 
		assert route , 'Empty strings are not allowed in shell'
		assert isinstance( delegated , int )
		
		if absolute: 
			assert __mod__.isabsolute( route ) , 'required absolute path, current is "%s"' % route

		if route.startswith('@'):

			if route in __mod__.TEMP_FILES:
				path = __mod__.TEMP_FILES[ route ]
			else:
				path = __mod__.join( tempfile.gettempdir() , next( tempfile._get_candidate_names() ) )
				__mod__.TEMP_FILES[ route ] = path

		elif __mod__.isabsolute( route ):
			path = __mod__.normalize( route )
		
		else:
			stack_offset = delegated + 1
			stack = inspect.stack() 
			f_path = os.path.abspath( stack[stack_offset][1] )

			if not route.strip():  #'empty string'
				'empty string, file'
				path = f_path
			else:
				'relative to folder'
				if os.path.exists( f_path ):
					head = os.path.dirname( f_path  )
				else:
					head = os.getcwd()
				path = __mod__.join( head , route )

		instance = str.__new__( cls , path )
		return instance

	def __getattr__( self , att ):

		'para evaluar metodos sin parametros utilizando la forma mayuscula'
		'ins.method(self) -> ins.METHOD'

		if att.isupper():
			if hasattr( self , att.lower() ):
				_method = getattr( self , att.lower() )
				return _method()
		
		return str.__getattribute__( self, att )

		#raise AttributeError , "%r object has no attribute %r (%r)" % (type(self).__name__, att , att.lower() )

	def __add__( self , other ):
		return type( self )( str(self) + other )



 ######  ##     ##     	##      ## ########     ###    ########   ######  
##    ## ##     ##     	##  ##  ## ##     ##   ## ##   ##     ## ##    ## 
##       ##     ##     	##  ##  ## ##     ##  ##   ##  ##     ## ##       
 ######  #########     	##  ##  ## ########  ##     ## ########   ######  
      ## ##     ##     	##  ##  ## ##   ##   ######### ##              ## 
##    ## ##     ##     	##  ##  ## ##    ##  ##     ## ##        ##    ## 
 ######  ##     ##     	###  ###  ##     ## ##     ## ##         ######  

	'Operaciones con argumentos, wrappers de os.path, shutils etc cuya operacion implique al fichero seleccionado'

	def relpath( self , root ):
		return __mod__.normalize( os.path.relpath( self , root ) )


	def isunder( self , parent ):

		if parent == self: return True

		'en este punto, parent solo puede ser un directorio'
		parent = type(self)( parent , delegated = True )
		parent = parent if parent.endswith('/') else parent + '/'

		if self.startswith( parent ):
			return True
		else:
			return False

	def steps( self , other ):

		'Devuelve una lista con al menos 2 elementos de menor a mayor'

		other = type(self)( other , delegated = True )
		paths = sorted( [ self , other ] , key = len )

		#sys.stderr.write( 'DEBUG %s\n' % paths )

		if paths[1]==paths[0]:
			return paths

		assert paths[1].isunder( paths[0] )

		'Limite de iteraciones' 
		for i in range(100): 
			cur = paths[1].PARENT
			if cur == paths[0]:
				break
			paths.insert( 1 , cur )

		return paths

	def tail( self , levels ):
		return '/'.join( self.split('/')[-levels:] )


	def chext( self , ext ):
		return self.PARENT( self.BASENAME + ext )

 ######  ##     ##   	########     ###    ######## ##     ## 
##    ## ##     ##   	##     ##   ## ##      ##    ##     ## 
##       ##     ##   	##     ##  ##   ##     ##    ##     ## 
 ######  #########   	########  ##     ##    ##    ######### 
      ## ##     ##   	##        #########    ##    ##     ## 
##    ## ##     ##   	##        ##     ##    ##    ##     ## 
 ######  ##     ##   	##        ##     ##    ##    ##     ## 


	def tagname( self ):
		return self.BASENAME.split('.')[0]

	def tagext(self):
		return self.BASENAME.replace( self.TAGNAME , '' , 1 )

	def tagsplit( self ):
		return self.TAGNAME,self.TAGEXT

	def tagroot( self ):
		return self.DIRNAME( self.TAGNAME )

	def name( self ): return os.path.splitext( self.BASENAME )[0]	
	def basename( self ): return os.path.basename( str(self) )
	def ext( self ): return os.path.splitext( self.BASENAME )[1]
	#def splitext( self ): return os.path.splitext( str(self) )
	
	def dirname( self ): 
		dname = os.path.dirname( str(self) )
		return type(self)( dname )
		
	parent = dirname

	def root(self):
		root = os.path.splitext( str(self) )[0]
		return type(self)( root )




	def exists( self ): 

		if re.findall('[\%\#]' , self.BASENAME ):
			return bool( self.GLOB )
		else:
			return os.path.exists( str(self) )

		
	def isfile( self ): return os.path.isfile( str(self) )
	
	def isdir( self ): return os.path.isdir( str(self) )


	def py_source( self ):

		'En el caso de una seleccion de py compilado, devuelve el py source'

		exts = [ '.py','.marshal','.pyc','.pyo']

		if self.EXT in exts:
			for ext in exts:
				py_path = self.chext( ext )
				if py_path.EXISTS:
					return py_path
		
		return self

	def py_compile( self ):
		
		if self.EXT == '.py':
			import py_compile
			py_compile.compile( self )
			mdl.log.debug( "shell( '%s' ).COMPILED" % self.BASENAME )
			return type(self)( self.ROOT + '.pyc' )

		return self


	def isbin( self ):
		assert self.ISFILE, "path is not a valid file : '%s'" % self
		return not self.ISTEXT

	def istext( self ):

		assert self.ISFILE, "path is not a valid file : '%s'" % self
		import mimetypes
		_type , _coding = mimetypes.guess_type( str(self) )
		if not _type or _type.startswith( 'text/' ):
			return True
		else:
			return False

	#def split( self ): return os.path.split( str(self) )	
	def stats( self ): 
		stats = os.stat( str(self) )[:]#[-2:]	
		#print 77777 , stats , os.stat( str(self) )[-3:-1]
		return stats

	def mtime( self ):
		return int(os.path.getmtime(self)*1000)
		#return os.stat( str(self) )[-2]


	def changed( self , delay = 3 ):

		'''Dice si un fichero ha cambiado desde la ultima vez que se ha accedido
		a esta funcion. El primer acceso siempre da positivo y los subsiguientes
		dependeran del delay ( para optimizar )

		'''

		assert self.EXISTS

		CACHE = mdl.uber.dictCache( 'Shell.changed' )
		
		cur_lapse = time.time() 
		lapse , mtime = CACHE.setdefault( self , (cur_lapse,0) )

		diff = cur_lapse - lapse
		if diff > delay:

			cur_mtime = self.MTIME 
			if mtime != cur_mtime:
				CACHE[ self ] = ( cur_lapse , cur_mtime )
				return True

		return False








 ######  ##     ##   	########  ########    ###    ########  
##    ## ##     ##   	##     ## ##         ## ##   ##     ## 
##       ##     ##   	##     ## ##        ##   ##  ##     ## 
 ######  #########   	########  ######   ##     ## ##     ## 
      ## ##     ##   	##   ##   ##       ######### ##     ## 
##    ## ##     ##   	##    ##  ##       ##     ## ##     ## 
 ######  ##     ##   	##     ## ######## ##     ## ########  
		
	@contextmanager
	def rb( self ):
		with open( self , 'rb' ) as f:
			yield f
	@contextmanager			
	def wb( self ):
		self.PARENT.MKDIR
		with open( self , 'wb' ) as f:
			yield f
	@contextmanager
	def r( self ):
		with open( self , 'rU' ) as f:
			yield f
	@contextmanager		
	def w( self ):
		self.PARENT.MKDIR
		with open( self , 'w' ) as f:
			yield f	

	@contextmanager		
	def a( self ):
		self.PARENT.MKDIR
		with open( self , 'a' ) as f:
			yield f	




	def read( self ):

		CACHE = mdl.uber.dictCache( 'Shell.read' )
		stats,data = CACHE.setdefault( self , (None,None) )
		
		#if stats != self.MTIME:
		with open( self ) as f:
			data = f.read().replace( '\r\n' , '\n').rstrip() + '\n'
			CACHE[self] = ( self.MTIME,data )
			#mdl.log.debug( "shell( '%s' ).READ" % self.BASENAME )

		return data

	def code(self):

		CACHE = mdl.uber.dictCache( 'Shell.code' )

		stats,data = items = CACHE.setdefault( self , [None,None] )
		
		if stats != self.MTIME:
			if self.ISTEXT:
				data = compile( self.READ , self , 'exec'  )

			elif self.ISBIN:

				with open( self , 'rb' ) as f:
					'tambien hace .marshal'
					if self.EXT in [ '.pyc' , '.pyo' ]: 
						f.read( 8 )
					data = marshal.load( f )
			
			else:

				raise RuntimeError, 'Extension MIME no reconcida . No es posible computar el codigo : %s' % self.__file__ 

			items[:] = [ self.MTIME,data ]
			#mdl.log.debug( "shell( '%s' ).CODE" % self.BASENAME )

		return data



 ######  ##     ##    ##        #######   ######  ##    ## 
##    ## ##     ##    ##       ##     ## ##    ## ##   ##  
##       ##     ##    ##       ##     ## ##       ##  ##   
 ######  #########    ##       ##     ## ##       #####    
      ## ##     ##    ##       ##     ## ##       ##  ##   
##    ## ##     ##    ##       ##     ## ##    ## ##   ##  
 ######  ##     ##    ########  #######   ######  ##    ## 


	@contextmanager		
	def lock( self , timeout = 10 , reclaim = 30 , sleep = .2  ):

		'Bloqueo local de archivos'
		'y si bloqueado vuelve a intentar bloquearlo?'
		
		self.MKFILE

		while 1:

			print 'waiting for lock...', self.BASENAME

			mtime = os.path.getmtime(self)
			atime = os.path.getatime(self)

			if mtime == 0:
				
				lapse = time.time() - atime

				if lapse > reclaim:
					print 'Reclaimed file lock (timeout): "%s"' % self.BASENAME
					break

				if lapse > timeout:
					raise RuntimeError('File access timeout: "%s"' % self.BASENAME)
				time.sleep( sleep )
				continue
			break
		


		os.utime( self , (time.time(),0) )
		try:
			print '--> Adquired Lock: "%s"' % self.BASENAME
			yield self
		
		finally:

			os.utime( self , None )
			print '<--  Release Lock: "%s"' % self.BASENAME
			time.sleep(0.1)


 ######  ##     ##  	######## ##     ##    ###    ##       
##    ## ##     ##  	##       ##     ##   ## ##   ##       
##       ##     ##  	##       ##     ##  ##   ##  ##       
 ######  #########  	######   ##     ## ##     ## ##       
      ## ##     ##  	##        ##   ##  ######### ##       
##    ## ##     ##  	##         ## ##   ##     ## ##       
 ######  ##     ##  	########    ###    ##     ## ######## 

	def module( self ):

		'Forma modular estatica'

		'Cached module namespace, no evalua nada'

		CACHE = mdl.uber.dictCache( 'Shell.module' )
		mod = CACHE.setdefault( str(self) , None )
		if mod == None:
			mod = types.ModuleType( '__mod__' ) #imp.new_module( '__mod__' )
			CACHE[ str(self) ] = mod
		return mod

	def mod( self ): #, **kwargs 

		'Forma modular dinamica a cambios'


		'Cache compartida con EVAL'
		CACHE = mdl.uber.dictCache( 'Shell.eval' )
		stats = CACHE.setdefault( str(self) , None )
		if stats != self.MTIME:
			self.EVAL
		return self.MODULE

	def ctx( self  ): #, **kwargs
		'Forma namespace dinamica a cambios'
		return vars( self.MOD )

	def ctx_clear( self ):
		self.CTX.clear()
		self.MODULE.__name__ = '__mod__'
		self.MODULE.__file__ = self
		self.MODULE.__doc__ = None
		self.MODULE.__package__ = None
		#self.MODULE.__mod__ = self.MOD

	def eval( self  ): #, **kwargs
		'La evaluacion es INCONDICIONAL, es decir siempre se debe evaluar por concepto'
	
		'Cache COMPARTIDA con MOD para los stats de evaluacion'
		CACHE = mdl.uber.dictCache( 'Shell.eval' )
		'cache antes de eval para que no redundee mod'
		CACHE[ self ] = self.MTIME

		self.CTX_CLEAR

		old_mod = sys.modules.get( '__mod__' , None )
		sys.modules['__mod__'] = self.MODULE

		try:
			'simple evaluacion en contexto'
			code = self.CODE
			ctx  = self.CTX
			eval( code , ctx )
			return self.MODULE


		except SystemExit as e:
			mdl.log.info( 'sys.exit desde la evaluacion de "%s" erno : %s' % ( self.BASENAME , e ) )

		except:
			'La evaluacion del modulo no es valida hasta que no produzca errores'
			CACHE[ self ] = None
			mdl.log.info( '! unsucessful eval of "%s"' % self.BASENAME )
			raise

		else:
			mdl.log.info( 'sucessful eval of "%s"' % self.BASENAME )
		finally:

			sys.modules.pop('__mod__')
			if old_mod: 
				sys.modules['__mod__'] = self.MODULE


	def tabbed_eval( self  ):


		stdout = sys.stdout
		stdout.flush() 

		current = sys.stdout 

		print "\n-> %s" % self.BASENAME
		sys.stdout = StringIO.StringIO() 
		try:
			self.EVAL
		finally:
			'get data'
			result = sys.stdout.getvalue()
			sys.stdout.close()
			'restore'
			sys.stdout = current
		
			result = '\n'.join( [ '\t' + l for l in result.split('\n') ] )
			
			print result.rstrip()
			print "<- %s" % self.BASENAME





 ######  ##     ##  	 #######  ########   ######  
##    ## ##     ##  	##     ## ##     ## ##    ## 
##       ##     ##  	##     ## ##     ## ##       
 ######  #########  	##     ## ########   ######  
      ## ##     ##  	##     ## ##              ## 
##    ## ##     ##  	##     ## ##        ##    ## 
 ######  ##     ##  	 #######  ##         ######  



	def chdir( self ):
		assert self.ISDIR
		os.chdir( self )
		return self

	def setcwd( self ):
		return self.CHDIR
	

	def make( self ):

		if self.EXT:
			self.MKFILE
		else:
			self.MKDIR

		return self

	def mkdir(self):

		if not self.EXISTS:
			os.makedirs( str(self) )
			#print '@ folder/s created : ' , self
		return self

	def mkfile(self):
		self.PARENT.MKDIR
		if not self.EXISTS:
			open( self , 'a' ).close()
		return self

	def touch( self ):
		
		"""Si el archivo no existe lo crea, si existe actualiza 
		el timestamp y como resultado el sistema creera que el 
		archivo ha cambiado.
		"""
		self.PARENT.MKDIR
		with open( self , 'a' ) as f:
			os.utime( self , None )
		return self

	def garbage(self):

		if self.EXISTS:
			trg = self.PARENT( '.garbage/%i' % time.time() ).MKDIR( self.BASENAME )
			os.rename( self , trg )
			print '@ garbage: ../%s' % trg.tail( 4 ) 
			return trg


	def cmp( self , other ):

		other = __mod__.Shell( other , delegated = True )
		return filecmp.cmp( self , other )

	
	def cp( self , dst , basename = None , overwrite = False ):

		src = self
		dst = __mod__.Shell( dst , delegated = True )

		if basename == None:
			dst = dst( self.BASENAME )
		else:
			dst = dst( basename )

		if shutil._samefile(src, dst):
			raise shutil.Error( "`%s` and `%s` are the same file" % (src, tmp_dst) )		

		#print 3334444 , 'shell.cp1' , dst 
		#print 3334444 , 'shell.cp2' , dst.PARENT

		dst.PARENT.MKDIR

		#Optimization
		buffer_size = min( 10485760 , os.path.getsize(src) ) or 1024 

		#No copia si son iguales
		if not overwrite and dst.ISFILE:
			if self.cmp( dst ):
				print 'Same file, no copy %s' % dst
				return dst 

		with open(src, 'rb') as fsrc:
			with open(dst, 'wb') as fdst:
				shutil.copyfileobj( fsrc, fdst, buffer_size )
				shutil.copystat( src, dst )

		return dst



 ######  ##     ##  	##      ##    ###    ##       ##    ## 
##    ## ##     ##  	##  ##  ##   ## ##   ##       ##   ##  
##       ##     ##  	##  ##  ##  ##   ##  ##       ##  ##   
 ######  #########  	##  ##  ## ##     ## ##       #####    
      ## ##     ##  	##  ##  ## ######### ##       ##  ##   
##    ## ##     ##  	##  ##  ## ##     ## ##       ##   ##  
 ######  ##     ##  	 ###  ###  ##     ## ######## ##    ## 


	def walk( self , hidden = False ):

		assert self.ISDIR, 'Not such folder to walk: %s' % self 
		'Pues eso, walk'
		for P,D,F in os.walk( self ):
			if not hidden:
				F[:] = [ f for f in F if not f.startswith('.') ]
				D[:] = [ d for d in D if not d.startswith('.') ]
			items = type(self)(P),D,F
			yield items

	def list_pyfiles( self ):

		'Da una lista NETA de los filenames python'

		done  = []
		exts  = ('.py','.pyc','.pyo','.marshal')
		pyfiles = []
		files = self.LIST_FILES
		for ext in exts:
			for f in files:
				n,e = os.path.splitext( f )
				if e == ext and n not in done:
					done.append( n )
					pyfiles.append( f )
		return sorted( pyfiles )

	def list_files( self ):
		for P,D,F in self.WALK: return F

	def list_folders( self ):
		for P,D,F in self.WALK: return D

	def listdir(self):
		return os.listdir( self )

	def glob( self ):

		'ordenacion por longitud y nombre'
		#key   = lambda i: len(i),i

		def key( item ):
			return -len(item),item

		iglob = glob.iglob( self.REPLACE_PADDING )
		'iglob devuelve un iterador'
		return sorted( [ type(self)(i) for i in iglob ] , key = key )


 ######  ##     ##  	 ######  ########  #######   ######  
##    ## ##     ##  	##    ## ##       ##     ## ##    ## 
##       ##     ##  	##       ##       ##     ## ##       
 ######  #########  	 ######  ######   ##     ##  ######  
      ## ##     ##  	      ## ##       ##  ## ##       ## 
##    ## ##     ##  	##    ## ##       ##    ##  ##    ## 
 ######  ##     ##  	 ######  ########  ##### ##  ######  

 	'''Podemos tener versiones _v01_
 	Podemos tener padding _###. .%04d.
 	

 	'''

#	def walk_sequences(self):
#
#		for P,D,F in self.WALK:
#
#			seqs = {}
#			'analiza todos los ficheros'
#			for f in F:
#				'Habra que evitar versiones supongo'
#				digits = re.findall( '.*?([0-9]+)' , f )
#				if digits:
#					padding = digits[-1]
#					pattern = ( '%0' + str(len(padding)) + 'd' ).join( f.rsplit( padding , 1 ) ) 
#					seqs.setdefault( pattern , [] ).append( int( padding ) )
#				else:
#					seqs[f] = None 
#
#			'saca las secuencias'
#			file_seqs = []
#
#			for pattern,pads in seqs.iteritems():
#
#				pads = sorted( pads )
#				if pads == None:
#					item = ( pattern , None ) 
#				else:
#					frange = ff,lf = pads[0] , pads[-1]
#					if ff == lf:
#						item = ( pattern % ff , None ) 
#					else:
#						'frange es una tuple, no como '
#						item = ( pattern , frange  ) 
#
#				file_seqs.append( item  )
#
#
#
#			yield P,D,sorted( file_seqs )
#

	def replace_hashes( self ): 

		'reemplaza ### por %03d'

		hashes = re.findall( '(\#+)' , self )
		if hashes:
			patt = hashes[-1]
			repl = '%%0%dd' % len( patt )
			return type(self)( self.replace( patt , repl ) )

		return self



	def replace_padding( self ):

		'Reemplaza %04d o ### por * para glob'

		pattern = r'(%+\d+d)|(#+)|(%d)'
		basename = re.sub( pattern , '[0-9]*' , self.BASENAME )
		return self.PARENT( basename )

#	def split_padding( self ):




 ######  ##     ##  	##     ## ######## ########   ######  
##    ## ##     ##  	##     ## ##       ##     ## ##    ## 
##       ##     ##  	##     ## ##       ##     ## ##       
 ######  #########  	##     ## ######   ########   ######  
      ## ##     ##  	 ##   ##  ##       ##   ##         ## 
##    ## ##     ##  	  ## ##   ##       ##    ##  ##    ## 
 ######  ##     ##  	   ###    ######## ##     ##  ######  

	'??? Las versiones solo funcionan cuando el directorio contiene la version'

	def version_tag( self ):

		matches = re.findall( '[/_.]v\d+' , self.NAME , re.IGNORECASE )  
		if len(matches):
			return self.NAME.split( matches[-1] )[0]


	
	'VERSION_NUMBER'

	def get_version( self ):

		matches = __mod__.match_versions( self )

		if len(matches):
			'current defined int version'
			return int( re.search("\d+", matches[-1] ).group() )


		
	def set_version( self, int_version ):

		matches = __mod__.match_versions( self )
		
		if len(matches):

			'change_version'
			vmatch = matches[-1]
			str_version = re.search( "\d+", vmatch ).group()
			padding = vmatch.replace( str_version , '%02d' ) #+ str(len(str_version)) +
			path = self
			for m in matches:
				new_version = padding % int_version
				path = new_version.join( path.rsplit( m ) )
			return __mod__.Shell( path )
			
		return self


	def decrease_version( self ):
		
		current_version = self.GET_VERSION
		if current_version == None: return self

		ver = 0 if current_version < 0 else current_version - 1
		return self.set_version( ver )

	def raise_version( self ):
		
		current_version = self.GET_VERSION
		if current_version == None: return self
		
		return self.set_version( current_version + 1 )

	def new_version( self ):

		if self.GET_VERSION == None: return self
		last = self.LAST_VERSION
		return last.RAISE_VERSION

	def first_version( self ):

		if self.GET_VERSION == None: return self
		result = self.set_version(0)
		return result.NEXT_VERSION


	def prev_version( self ):

		if self.GET_VERSION in [ None , 0 ] : return self
		
		#print 'GETTING PREV VERSION OF: ' , self

		prev = self
		while 1:
			prev = prev.DECREASE_VERSION
			#print 777, prev
			if prev.PARENT.EXISTS:
				if prev.EXISTS:
					break
			if prev.GET_VERSION == 0:
				return prev
		return prev

	def next_version( self ):

		cur_ver = self.GET_VERSION
		if cur_ver == None: return self

		#print 'GETTING NEXT VERSION OF: ' , self

		next = self
		#diff = 0
		#while 1:
		for i in range( 100 ):
			next = next.RAISE_VERSION
			if next.PARENT.EXISTS:
				if next.EXISTS:
					return next
					#break
#			diff += 1
#			if diff > ( cur_ver + 100 ):
#				return self
		return self
#		return next



	'Como de agresivo seria empezar en la version 0 y tirar para adelante?'

	def last_version( self ):
		
#		next = self.NEXT_VERSION
#		
#		if next == self and next.EXISTS:
#			return self		
#		elif next.EXISTS:
#			return next.LAST_VERSION
#		else:
#			return self.PREV_VERSION
		
		#print 'GETTING LAST VERSION OF: ' , self

		if self.GET_VERSION == None: return self

		next = self.NEXT_VERSION
		if next.EXISTS:
			if next == self:
				result =  next
			else:
				result =  next.LAST_VERSION
		else:
			result = self.PREV_VERSION

		#print 'RESULT LAST VERSION OF: ' , result

		return result
				
#		cache = mdl.uber.dictCache('LASTS').setdefault( 'items' , [] )
#
#		if self not in cache:
#
#			cache.append( self )
#
#		
#
#		result = self.set_version(0)
#
#		while 1:
#			next = result.NEXT_VERSION
#			if next == result:
#				break
#			result = next
#
#		return result










 ######  ##     ##       ##     ## ######## #### ##        ######  
##    ## ##     ##       ##     ##    ##     ##  ##       ##    ## 
##       ##     ##       ##     ##    ##     ##  ##       ##       
 ######  #########       ##     ##    ##     ##  ##        ######  
      ## ##     ##       ##     ##    ##     ##  ##             ## 
##    ## ##     ##       ##     ##    ##     ##  ##       ##    ## 
 ######  ##     ##        #######     ##    #### ########  ######  






'solo mutables'
def dict_cache( tag ):
	return vars( __mod__ ).setdefault( '__cache__' , {} ).setdefault( tag , {} )






def match_versions( path ):

	matches = re.findall( '[/_.]v\d+' , path , re.IGNORECASE )  
	if len(matches):
		last_version = matches[-1]
		matches = [ m for m in matches if m == last_version ]
		return matches
	else:
		return []



def normalize( path ):

	assert isinstance( path , (str,unicode) ),'Current type is %s' % type(path)
	path = str( path )
	'Normalize the path with / separator'
	path = os.path.expandvars( os.path.expanduser( path ) )
	path = os.path.normpath( path )

	path = path.replace( '\\' , '/' )#.rstrip(  '/' )

	if path.endswith( '/' ): 
		path = path[:-1]
	if path.endswith( ':' ) or not path: 
		path += '/'

	return path


def caller():

	stack = inspect.stack()
	ctx = stack[2][0].f_globals
	if ctx == __mod__.Shell.__getattr__.func_globals:
		ctx = stack[3][0].f_globals		
	return ctx




def isabsolute( path ):

	path = __mod__.normalize( path )
	if path.startswith('/') or path[1:2]==':':
		return True
	return False




def join( head , tail ):

	tail = __mod__.normalize( tail )
	head = __mod__.normalize( head )

	'is absolute?'
	if __mod__.isabsolute( tail ):
		return tail

	path = os.path.join( head,tail)
	path = os.path.abspath( path )
	path = __mod__.normalize( path )

	return path


def has_changed( path , tag ):

	path = os.path.splitext(path)[0] + '.py'
	path = __mod__.normalize( path )

	if os.path.exists( path ):

		cur_lapse = time.time()

		CHANGED = mdl.uber.dictCache( 'shell.has_changed' ).setdefault( tag , {} )

		lapse , mtime = CHANGED.setdefault( path , ( cur_lapse , 0 ) )			

		diff = cur_lapse - lapse
		
		if diff > 5:
			
			cur_mtime = int(os.path.getmtime(path)*1000)
			if mtime != cur_mtime:
				CHANGED[ path ] = ( cur_lapse , cur_mtime )
				return True

		return False





