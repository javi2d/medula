
import time
import inspect
import types
import os
import pprint
import mimetypes
import marshal
import ast
import traceback
import threading

import __main__

'logging'
import logging
log = logging.getLogger(__name__)

import sys

'Este modulo es eminentemente ESTATICO'

from contextlib import contextmanager



__mod__ = sys.modules[__name__]

#PARMOD = inspect.getmodule( inspect.stack()[0][0] )
'Esta cache es persistente incluso en recargas de modulo'
CACHE = vars( __mod__ ).setdefault( '__cache__' , {} )
DEVMODE = True 
DELAY = 1 #secs to check if file has changed


##     ## ######## #### ##        ######  
##     ##    ##     ##  ##       ##    ## 
##     ##    ##     ##  ##       ##       
##     ##    ##     ##  ##        ######  
##     ##    ##     ##  ##             ## 
##     ##    ##     ##  ##       ##    ## 
 #######     ##    #### ########  ######  


'caches'
def dictCache( tag ):
	return vars( __mod__ ).setdefault( '__dictCache__' , {} ).setdefault( tag , {} )

def listCache( tag ):
	return vars( __mod__ ).setdefault( '__listCache__' , {} ).setdefault( tag , [] )


'profiler'
@contextmanager
def profile( msg ):
	lapse = time.time()
	yield
	msecs = ( time.time() - lapse )*1000	
	__mod__.log.info( '[%s] profile takes %s msecs' % (msg,msecs)  )



'exceptions'
def print_exception( tabs = 0 ):

	sys.stderr.write( __mod__.format_exception( tabs ) + '\n' )


def format_exception( e = None , tabs = 0 ):
	
	tabs = '\t'*tabs
	result = ('\n'+tabs).join( traceback.format_exc().split('\n') )
	result = result.replace('\t','    ')
	return result


def format_dict( dic , hidden = False , limit = True ):

	items  = sorted( dic.items() )

	def lines():

		for k,v in items:

			k = k.rjust(12)
			v = repr( v )
			
			if limit and len(v)>107:
				v = '%s (...) %s' % ( v[:50].rstrip() , v[-50:].lstrip() )

			yield '%s = %s' % (k,v)

	sep = '\n\t'
	
	result = sep + sep.join( lines() ) + '\n' 
	result = result.replace('\t','    ')

	return result


def debug( *args , **kwargs ):

	stack = inspect.stack()[1]
	template = '\n[UBER_DEBUG]' + ' %s ' + 'in < %s > line %d of file "%s"\n' % stack[1:4][::-1]

	if not args:
		msg = ( template % 'locals()' ) + __mod__.format_dict( stack[0].f_locals , **kwargs )		

	else:
		
		msg = ''

		for obj in args:

			_type = type( obj ).__name__
			
			if not isinstance( obj , dict ):
				obj = vars( obj )

			msg += ( template % _type ) + __mod__.format_dict( obj , **kwargs )		


	return msg






#
#def debug_dict( d , hidden = False , limit = True  ):
#	
#	stack = inspect.stack()[1]
#	msg  = '\nDebug Dict < %s > line %d of file "%s"\n' % stack[1:4][::-1] 
#	
#	return msg + __mod__.format_dict( d , hidden , limit  )
#
#def debug_vars( obj , hidden = False , limit = True  ):
#	
#	stack = inspect.stack()[1]
#	msg  = '\nDebug Vars < %s > line %d of file "%s"\n' % stack[1:4][::-1] 
#	
#	return msg + __mod__.format_dict( vars(obj) , hidden , limit  )
#
#
#def debug_locals( delegated = 0 , hidden = False , limit = True  ):
#
#	offset = delegated + 1
#	stack = inspect.stack()[offset]
#	msg = '\nDebug Locals in < %s > line %d of file "%s"\n' % stack[1:4][::-1] 
#	
#	return msg + __mod__.format_dict( stack[0].f_locals , hidden , limit )


def flush_buffers( out = True , err = True ):

	if out:
		sys.stdout.flush()
		sys.__stdout__.flush()	

	if err:
		sys.stderr.flush()
		sys.__stderr__.flush()	




######## ##     ##  ######  ######## ########  ######## ####  #######  ##    ## 
##        ##   ##  ##    ## ##       ##     ##    ##     ##  ##     ## ###   ## 
##         ## ##   ##       ##       ##     ##    ##     ##  ##     ## ####  ## 
######      ###    ##       ######   ########     ##     ##  ##     ## ## ## ## 
##         ## ##   ##       ##       ##           ##     ##  ##     ## ##  #### 
##        ##   ##  ##    ## ##       ##           ##     ##  ##     ## ##   ### 
######## ##     ##  ######  ######## ##           ##    ####  #######  ##    ## 



class uberException( Exception ):

	def __init__( self , msg = '' ):

		exc_info = sys.exc_info()
		
		args =  exc_info[0].__name__ , exc_info[1].message , msg

		self.message = '-> %s: %s\n%s' % args
		
	def __str__( self ):		
		return self.message


######## ##     ## ########  ########    ###    ########  
   ##    ##     ## ##     ## ##         ## ##   ##     ## 
   ##    ##     ## ##     ## ##        ##   ##  ##     ## 
   ##    ######### ########  ######   ##     ## ##     ## 
   ##    ##     ## ##   ##   ##       ######### ##     ## 
   ##    ##     ## ##    ##  ##       ##     ## ##     ## 
   ##    ##     ## ##     ## ######## ##     ## ########  


def uberThread( fun , *args , **kwargs ):

	thread = threading.Thread( None , fun , args = args , kwargs = kwargs )
	return thread

def uberDaemon( *args , **kwargs ):

	thread = __mod__.uberThread( *args , **kwargs )
	thread.daemon = True
	return thread






##     ## ########  ######## ########  ########   #######   ######   ######  
##     ## ##     ## ##       ##     ## ##     ## ##     ## ##    ## ##    ## 
##     ## ##     ## ##       ##     ## ##     ## ##     ## ##       ##       
##     ## ########  ######   ########  ##     ## ##     ## ##        ######  
##     ## ##     ## ##       ##   ##   ##     ## ##     ## ##             ## 
##     ## ##     ## ##       ##    ##  ##     ## ##     ## ##    ## ##    ## 
 #######  ########  ######## ##     ## ########   #######   ######   ######  


class uberGenerator( object ):

	pass
	'Hacerlo con el send que tenga timeout y que no bloquee'



class uberDocs( ast.NodeVisitor ):

	"""Hay que mirar cadenas anonimas triple quoted y 
	revisar su contexto para saber a que se refiere"""

#	CACHE = {} #la carga doble puede ser por esto y el ubermodule

	def __new__( cls , path ):

		import mdl

		'restaurar'
		self = super( uberDocs,cls).__new__(cls)
		
		self.path = mdl.shell( path , delegated = True )
		self.struct = []
		self.level  = 0
		self.lineno = 0

		node = ast.parse( self.path.READ , self.path , 'exec' )
		
		self.visit( node )
		
		return self.struct

	def generic_visit( self , node ):


		if hasattr( node , 'lineno' ):
			if node.lineno > self.lineno:
				self.lineno = node.lineno
				print '\n%04d\n' % self.lineno

		#print ast.dump( node )

		#print node

		childs = list( ast.iter_child_nodes(node) )

		
		'esto esta ok'
#		if isinstance( node , (ast.FunctionDef , ast.ClassDef , ast.Module) ):
#			
#			info_fields = ','.join( node._fields ).split('body')[0].split(',')
#			info_fields.pop()
#			print info_fields
#
#
#			for field in info_fields:
#				print field , getattr( node , field )
#
#			print ast.get_docstring( node )
#
#		return super( uberDocs,self ).generic_visit( node )


def uberContext( *args ):

	f_locals = inspect.stack()[1][0].f_locals
	items = [ i for i in f_locals.iteritems() if i[0] in args ] 
	return dict( items )




##     ## ########  ######## ########  ##     ##  #######  ########  
##     ## ##     ## ##       ##     ## ###   ### ##     ## ##     ## 
##     ## ##     ## ##       ##     ## #### #### ##     ## ##     ## 
##     ## ########  ######   ########  ## ### ## ##     ## ##     ## 
##     ## ##     ## ##       ##   ##   ##     ## ##     ## ##     ## 
##     ## ##     ## ##       ##    ##  ##     ## ##     ## ##     ## 
 #######  ########  ######## ##     ## ##     ##  #######  ########  


def uberModule( module = None , ctx = None ): #, 

	'Esta funcion no puede utilizar mdl'

	module = module or inspect.getmodule( inspect.stack()[1][0] )
	
	if module == __mod__: raise RuntimeError('uber es un modulo estatico (shell.EVAL)')

	if module == None:
		raise RuntimeError('''
			uber.uberModule no puede utilizarse desde la 
			sesion interactiva de python sin especificar 
			un modulo.

			uber.uberModule( module )

			''')

	'Aqui __main__ sale explicitamente de un archivo  $ python xx.py y si que lo reconoce como modulo'
	
	if module.__name__ == '__main__':

		if os.path.isfile( module.__file__ ):
			
			print 'INFO uberModule: Importando el fichero asociado an namespace __main__ -> %s' % module.__file__
			module = __import__( inspect.getmodulename( module.__file__ ) )
			
		else:
			raise RuntimeError( 'No esta permitido hacer un uberModulo si __file__ no es un archivo valido' )
		
		'si tras este reajuste no logramos reconocer el modulo salta un error'
		if module.__name__ == '__main__': 
			raise RuntimeError( 'No esta permitido hacer un uberModulo desde la consola, debe estar asociado a un archivo valido.' )


	

	if type( module ).__name__ == 'module': #'UberModule'



		#print 'uber? :: ' , inspect.getmodulename( module.__file__ ) , module , module.__file__

		ctx = dict( vars( module ) if ctx == None else ctx )

		class UberModule( types.ModuleType ):

			'en el momento de declaracion todo lo que haya definido se convierte en clsattrib'
			
			vars().update( ctx )

			#print __mod__.debug_dict( ctx )
			def __init__( self , name ):

				#super( UberModule,self ).__init__( name )
				types.ModuleType.__init__( self , name )
				'hacemos el __init__ de usuario despues de inicializar el modulo'
				if '__init__' in ctx: ctx['__init__']( self )

				'almacenamos las stats del modulo para la recarga'
				__mod__.store_mtime( module.__file__ )

			def __dir__( self ):

				if '__dir__' in ctx: 
					return ctx['__dir__']( self )

				return list( vars( self ).keys() + vars( module ).keys()  ) 

			def __getattribute__( self , att ):

				#print 'Cogiendo Atributo de uber -> "%s"' % att
				
				if '__getattribute__' in ctx:
					#raise RuntimeError , 'No se puede redefinir __getattribute__ en un ubermodule'
					return ctx['__getattribute__']( self , att )
				
				try:

					'Acceso al valor en la clase padre si este existe'
					value = super( UberModule,self ).__getattribute__( att )
					#value = types.ModuleType.__getattribute__( self, att )

				except:

					has_changed = __mod__.has_changed( module.__file__ ) #True  else 

					if att == '@' : has_changed = True

					'Si el fichero ha cambiado recarga el modulo sobre si mismo'
					if __mod__.DEVMODE and has_changed:
						sys.__stdout__.write( '\n@ uberModule reload -> "%s"\n\n' % module.__name__ )
						execfile( module.__file__  , vars( module ) )

						'almacenamos las stats del modulo para la recarga'
						__mod__.store_mtime( module.__file__ )

						'la actualizacion de special methods es un lio'

					if att == '@' : 
						value = None
					else:
						value = getattr( module , att )


					#value = ( None if att == '@' else getattr( module , att ) )

				return value

			def __setattr__( self , k , v ):

				#'''Esto vale para que si el usuario crea un atributo NUEVO en el modulo
				#que no existe en el modulo original el atributo se crea en la clase 
				#haciendolo persistente
				#'''
				#'Si se modifica un atributo de forma explicita __mod__.att = XXXX'

				'Si el atributo existe el el contexto original se sobreescribe en la clase'
				'si no se hace volatil para que no se acumule mierda que ya existe durante'
				'las recargas.'

				#print '...setting att', k , k in ctx 

				if k in ctx:
					types.ModuleType.__setattr__( self , k , v )
	
				setattr( module , k , v )

#				print '...setting attribute' , k , sorted( ctx.keys() )

#				if k in vars( module ):
#					setattr( module , k , v )
#				else:
#					#super( UberModule,self ).__setattr__( k , v )
#					types.ModuleType.__setattr__( self , k , v )
#
		sys.modules[ module.__name__ ] = UberModule( module.__name__ )
		__mod__.log.info( "+ubermodule '%s'" % module.__name__ )

	return sys.modules[ module.__name__ ]


def path_mtime( path ):
	return int( os.path.getmtime(path)*1000 )


def store_mtime( path ):
	__mod__.CACHE[ path ] = ( time.time() , __mod__.path_mtime( path ) )



def has_changed( path ):

	'Esta funcion no puede utilizar mdl'

	path = os.path.splitext(path)[0] + '.py'
	if not os.path.exists( path ): 
		__mod__.log.warn( 'ubermodule has_changed path not exists %s' % path)
		return False

	lapse = time.time()
	
	'ya debe existir por que se crea cuando se crea el ubermodule'
	last_lapse , last_mtime = __mod__.CACHE[path] ##__mod__.CACHE.setdefault( path , ( lapse , None ) )

	'Incrementa la agilidad de la funcion'
	diff = ( lapse-last_lapse )
	if diff < __mod__.DELAY: 
		return False 
	
	'no recargamos si ya hemos cargado esa definicion'
	if __mod__.path_mtime( path ) == last_mtime : 
		return False

	print 'ubermod ha cambiado'
	'Cuando la nueva recarga se realice correctamente se almacenan los nuevos datos'

	return True


##     ## ########  ######## ########   ######     ###    ##       ##       
##     ## ##     ## ##       ##     ## ##    ##   ## ##   ##       ##       
##     ## ##     ## ##       ##     ## ##        ##   ##  ##       ##       
##     ## ########  ######   ########  ##       ##     ## ##       ##       
##     ## ##     ## ##       ##   ##   ##       ######### ##       ##       
##     ## ##     ## ##       ##    ##  ##    ## ##     ## ##       ##       
 #######  ########  ######## ##     ##  ######  ##     ## ######## ######## 


def uberCallable( obj ):

	__mod__ = inspect.getmodule( inspect.stack()[1][0] )

	if type( __mod__ ).__name__ == 'UberModule':
		setattr( type(__mod__) , '__call__' , staticmethod(obj) )

	return obj


##     ## ########  ######## ########   ######  ##        ######  
##     ## ##     ## ##       ##     ## ##    ## ##       ##    ## 
##     ## ##     ## ##       ##     ## ##       ##       ##       
##     ## ########  ######   ########  ##       ##        ######  
##     ## ##     ## ##       ##   ##   ##       ##             ## 
##     ## ##     ## ##       ##    ##  ##    ## ##       ##    ## 
 #######  ########  ######## ##     ##  ######  ########  ######  

class uberClass(type):
	
	'metaclass'

	def __new__( mcls, name, bases, ctx ):

		__mod__ = inspect.getmodule( inspect.stack()[1][0] )
		
		if type( __mod__ ).__name__ == 'UberModule':

			#__uber__ = uberModule( __mod__ )

			assert '__getattribute__' not in ctx , 'Unable to uberClass this object, __getattribute__ already defined'
		
			def __getattribute__( self , att ):

				if att in ctx and not ( att.startswith( '__' ) and att.endswith('__') ):

					'Esto hace el reload'
					obj = getattr( __mod__ , name )
					mth = getattr( obj , att )

					if isinstance( mth , types.UnboundMethodType ) :

						attribute = mth.__get__( self , obj )
						return attribute

				'Delega en el atributo original'
				attribute = object.__getattribute__(self, att )
				return attribute

			
			ctx['__getattribute__'] = __getattribute__
			cls = type( name , bases , ctx )

			return cls




##     ## ########  ######## ########   #######  ########        ## 
##     ## ##     ## ##       ##     ## ##     ## ##     ##       ## 
##     ## ##     ## ##       ##     ## ##     ## ##     ##       ## 
##     ## ########  ######   ########  ##     ## ########        ## 
##     ## ##     ## ##       ##   ##   ##     ## ##     ## ##    ## 
##     ## ##     ## ##       ##    ##  ##     ## ##     ## ##    ## 
 #######  ########  ######## ##     ##  #######  ########   ######  


class uberObject( object ):

	'Hibrido objeto/diccionario'

	def __lshift__( self , other ):
		self.__dict__.update( other )
		return self

	def __str__( self ):
		return pprint.pformat( dict(self), indent=2, width=80, depth=None)

	def __getitem__( self , key ):

		if key == slice(None):
			return self.__dict__
		return self.__dict__.__getitem__( key )

	def __setitem__( self , key , val ):
		self.__dict__.__setitem__( key, val )

	def __contains__( self , key ):
		return key in dict( self )

	def __iter__( self ):
		for i in self.__dict__.iteritems():
			yield i

	def __dir__( self ):
		'pasa por __iter__ y lo devuelve filtrado'
		return dict( self ).keys()


##     ## ########  ######## ########   ######  ########    ###    
##     ## ##     ## ##       ##     ## ##    ##    ##      ## ##   
##     ## ##     ## ##       ##     ## ##          ##     ##   ##  
##     ## ########  ######   ########   ######     ##    ##     ## 
##     ## ##     ## ##       ##   ##         ##    ##    ######### 
##     ## ##     ## ##       ##    ##  ##    ##    ##    ##     ## 
 #######  ########  ######## ##     ##  ######     ##    ##     ## 

def uberStatic( obj ):

	'decorador para convertir todos los metodos de una clase en metodos estaticos'

	ctx = vars( obj )
	for k,v in ctx.iteritems():
		if isinstance( v , types.FunctionType ):
			ctx[k] = staticmethod( v )
		
	return obj



