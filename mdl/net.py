



import time
import os
import sys
import threading
import random

import SocketServer
import json
import socket
import errno
import atexit
import traceback
import subprocess 
import inspect

import tempfile


try:
	import cStringIO as StringIO
except:
	import StringIO

import marshal
try:
	import cPickle as pickle
except:
	import pickle

import urllib
from HTMLParser import HTMLParser
import re

from contextlib import contextmanager

import ast
import select


import mdl


LOCK = threading.RLock()
ATTEMPTS = 5

'Este modulo requiere uber'
__mod__ = mdl.uber.uberModule()



##     ## ######## ##     ## ##       
##     ##    ##    ###   ### ##       
##     ##    ##    #### #### ##       
#########    ##    ## ### ## ##       
##     ##    ##    ##     ## ##       
##     ##    ##    ##     ## ##       
##     ##    ##    ##     ## ######## 



def html( tags , value , **kwargs ):

	"html( 'center,b,font' ,   )"

	tags = [ i.strip() for i in tags.split(',') if i.strip() ]
	
	tag = tags.pop()
	
	defaults = {}

	value = str( value ).replace( '\n' , '<br>')

	if tag == 'font':

		defaults = dict( size = 3 , 
						 color = 'Black', 
						 face = 'Consolas,Lucida,Verdana,Monaco,Arial,Courier,',)
	if tag == 'img':
		defaults = dict( width = 3 ) 

	defaults.update(kwargs)

	params = ' ' + ' '.join([ '%s="%s"' % (k,v) for k,v in defaults.iteritems() ])

	result = '<%s%s>%s</%s>' % ( tag , params , value , tag )

	while tags:	
		tag = tags.pop()
		result = __mod__.html( tag , result )

	#print 'html_result' , result

	return result


		



#### ##    ## ########  #######  
 ##  ###   ## ##       ##     ## 
 ##  ####  ## ##       ##     ## 
 ##  ## ## ## ######   ##     ## 
 ##  ##  #### ##       ##     ## 
 ##  ##   ### ##       ##     ## 
#### ##    ## ##        #######  

def ip():
	return socket.gethostbyname( socket.gethostname() )

def hostname( normalize = True ):
	hostname = socket.gethostname()
	if normalize:
		hostname = hostname.split('.')[0].upper()
	return hostname

def login():
	return os.path.basename( os.path.expanduser('~') )


def available_port():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',0))
	port = sock.getsockname()[1]
	return port


def pid():

	return str( os.getpid() )


def network_id():

	'network id, cadena de 16 caracteres'
	return '%s.%s' % ( os.getpid() , threading.currentThread().ident )


def public_ip():

	found_ips = []

	#public_ip.ip = ''

	# create a subclass and override the handler methods
	class MyHTMLParser(HTMLParser):
		def handle_data(self, data):
			#print data
			pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
			if pat.match(data):
				found_ips.append( data )
				#self.close()

	MyHTMLParser().feed( urllib.urlopen('http://whatismyip.org').read() )

	return found_ips


 ######   #######   ######  ##    ## 
##    ## ##     ## ##    ## ##   ##  
##       ##     ## ##       ##  ##   
 ######  ##     ## ##       #####    
      ## ##     ## ##       ##  ##   
##    ## ##     ## ##    ## ##   ##  
 ######   #######   ######  ##    ## 


@contextmanager
def sock( address ):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(address)
	except:
		raise RuntimeError ,  'Error conectando al servidor'
	try:
		yield s
	except Exception,e:
		raise RuntimeError ,  'Error durante el uso del socket : %s' % e
	finally:
		s.close()
		



########   #######  ##     ## ######## #### ##    ## ######## 
##     ## ##     ## ##     ##    ##     ##  ###   ## ##       
##     ## ##     ## ##     ##    ##     ##  ####  ## ##       
########  ##     ## ##     ##    ##     ##  ## ## ## ######   
##   ##   ##     ## ##     ##    ##     ##  ##  #### ##       
##    ##  ##     ## ##     ##    ##     ##  ##   ### ##       
##     ##  #######   #######     ##    #### ##    ## ######## 

#def raise_exception( msg = '' , note = '' ):
#	
#	err = mdl.uber.format_exception( tabs = 1 )
#
#	if msg: err = '\n'+msg+err 
#	if note: err = err+'\n'+note
#	
#	sys.__stderr__.flush()
#	sys.__stderr__.write( err + '\n' )
#	
#	return sys.exc_info()[1]



def recv_size( s ):
	'los primeros 1024 bytes son la longitud de los datos'
	str_size = s.recv( 1024 )
	int_size = int( str_size )
	return int_size


def recv( s , int_size ):
	data = s.recv( int_size )
	data_obj = pickle.loads( data )
	return data_obj


def send( s , data_obj ):

	data = pickle.dumps( data_obj )
	str_size = str(len(data)).zfill(1024)
	s.sendall( str_size )
	s.sendall( data )	




def read_address( link ):

	link = mdl.shell( link , delegated = 1 )
	'read address'
	with link.R as f: txt = f.read().strip()
	
	address = ast.literal_eval( txt )	
	
	return address


def new_address():

	return __mod__.ip() , __mod__.available_port() 





 ######  ######## ########  ##     ## ######## ########  
##    ## ##       ##     ## ##     ## ##       ##     ## 
##       ##       ##     ## ##     ## ##       ##     ## 
 ######  ######   ########  ##     ## ######   ########  
      ## ##       ##   ##    ##   ##  ##       ##   ##   
##    ## ##       ##    ##    ## ##   ##       ##    ##  
 ######  ######## ##     ##    ###    ######## ##     ## 


		
class Server( SocketServer.ThreadingTCPServer ):
	
	allow_reuse_address = True
	
	def __init__( self , link , module , methods = [] ):
		
		self.link = mdl.shell( link , delegated = 1 )


		'Si el fichero existe no lanzar uno nuevo???'

		self.address = __mod__.new_address()
		self.methods = methods	
		self.module = module

		#self.lock = threading.RLock()
		
		srv = self

		class Handler(SocketServer.BaseRequestHandler):
			
			LOCK = threading.RLock()

			def handle(self):
				'asi parece que actualiza mas rapido'
				handler = getattr( __mod__ , 'server_handler' )
				handler( self , srv )

		#print mdl.uber.debug( self )
		SocketServer.ThreadingTCPServer.__init__( self, self.address , Handler )

		print '[ SERVER INFO ]: New UNSTARTED server instance at %s with module "%s" with link "../%s"' % ( self.address , self.module.__name__ , self.link.tail(4) )
	
	def start( self ):

		sys.__stdout__.flush()

		print '[ SERVER INFO ]: dumping server link file "../%s"' %  self.link.tail(4)
		with self.link.W as f: f.write( repr( self.address ) )		

		print '[ SERVER INFO ]: started at (%s,%s), press ctrl+c to exit' % self.address
		try:
			self.serve_forever()
		except KeyboardInterrupt:
			print '[ SERVER INFO ]: server KeyboardInterrupt stop %s@%s' % self.address
		except SystemExit:
			print '[ SERVER INFO ]: server SystemExit stop %s@%s' % self.address

		return


 ######  ########  ##     ##       ##     ## ########  ##       ########  
##    ## ##     ## ##     ##       ##     ## ##     ## ##       ##     ## 
##       ##     ## ##     ##       ##     ## ##     ## ##       ##     ## 
 ######  ########  ##     ##       ######### ##     ## ##       ########  
      ## ##   ##    ##   ##        ##     ## ##     ## ##       ##   ##   
##    ## ##    ##    ## ##         ##     ## ##     ## ##       ##    ##  
 ######  ##     ##    ###          ##     ## ########  ######## ##     ## 

#class ServerException( Exception ): pass

def server_handler( self , srv ):


	lapse = time.time()

	if not srv.link.ISFILE or srv.address != __mod__.read_address( srv.link ):
		srv.shutdown()
		return True

	#print '.',

	#print '@HANDLE %s' % srv.link.NAME

	'entrada'
	try:

		s = self.request

		'recv_size'
		int_size = __mod__.recv_size( s )
		#print '@srv.recv_size:'.ljust( RJUST ) , int_size
		
		'breakpoint with no data, NO databack'
		if int_size == 0: return
		
		'recv'
		data_obj = __mod__.recv( s , int_size )
		#print '@srv.recv:'.ljust( RJUST ) , repr( data_obj )

		'separate data'
		att, args, kwargs = data_obj

	except: #Exception, e

		print '[ REMOTE SERVER ERROR ]: Error recibiendo el mensaje del cliente'
		print mdl.uber.format_exception()

		__mod__.send( s , sys.exc_info()[1] )

		return

	else:
		
		'salida'
		try:

			'process'
			with __mod__.LOCK:
				#srv.module.__name__
				#print '[ SERVER INFO ]: Getting attribute "%s" from srv.module %s' % ( att , srv.module ) 
				method = getattr( srv.module , att )
				#print '[ SERVER INFO ]: Getting result of "%s(%s,%s)"' % ( att , args, kwargs ) 
				result = method( self , *args , **kwargs ) 

		except Exception, e:
			
			#err = __mod__.raise_exception( msg )
			print '\n[ REMOTE SERVER ERROR ]: Problema con la evaluacion del atributo remoto "%s(%s,%s)"' % ( att , args, kwargs )
			print mdl.uber.format_exception()

			__mod__.send( s , sys.exc_info()[1] )
			#__mod__.send( s , err )			
			return

		else:
			'send'
			__mod__.send( s , result )




 ######  ##       #### ######## ##    ## ######## 
##    ## ##        ##  ##       ###   ##    ##    
##       ##        ##  ##       ####  ##    ##    
##       ##        ##  ######   ## ## ##    ##    
##       ##        ##  ##       ##  ####    ##    
##    ## ##        ##  ##       ##   ###    ##    
 ######  ######## #### ######## ##    ##    ##    




def fileSocket( path , timeout = None  ):

	path = mdl.shell( path , delegated = 1 )

	address = __mod__.read_address( path )
	
	'test connection, like ping'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout( timeout )
	s.connect( address )
	return s



class Client( object ):
		
	'El cliente no tiene atributos por que los relega a los definidos por el modulo del servidor'

	def __init__( self , path ):
		'el path indica la direccion del servidor'	
		self.__file = mdl.shell( path , delegated = 1 )

	def __nonzero__( self ):

		if not self.__file.ISFILE: 
			return False
		try:
			s = __mod__.fileSocket( self.__file, timeout = 3 )	
		except:
			return False
		try:
			s.send( '0'*1024 )
			return True			
		except:
			return False
		finally:
			s.close()

	def __getattribute__( self,att ): #ping

		try:
			return super( Client,self ).__getattribute__( att )
		except:

			if not self.__file.ISFILE:
				raise RuntimeError('No such server file %s' % self.__file.BASENAME )

			s = __mod__.fileSocket( self.__file , timeout = 15 )

			'intermediate'
			intermediate = __mod__.client_handler( s , att )
			#print '@proxy.%s' % att
			return intermediate	





 ######  ##       ####       ##     ## ########  ##       ########  
##    ## ##        ##        ##     ## ##     ## ##       ##     ## 
##       ##        ##        ##     ## ##     ## ##       ##     ## 
##       ##        ##        ######### ##     ## ##       ########  
##       ##        ##        ##     ## ##     ## ##       ##   ##   
##    ## ##        ##        ##     ## ##     ## ##       ##    ##  
 ######  ######## ####       ##     ## ########  ######## ##     ## 



RJUST = 20

def client_handler( s , att ):
	
	s,att = s,att

	def client_proxy( *args , **kwargs ):
		
		sys.__stdout__.flush()

		'envio'

		try:

			data_obj = [ att , args , kwargs ]

			'send'
			__mod__.send( s,data_obj )
			#print '@cli.sendall:'.ljust( RJUST ) , repr( data_obj )

		except:

			print '\n[ CLIENT ERROR ]: Error enviando el mensaje al servidor ->'
			print  mdl.uber.format_exception()

			#__mod__.raise_exception( msg )
			#print mdl.uber.format_exception( msg , e  )
			#mdl.uber.format_exception( '@Error en cliente en el envio de los datos' , e  )

		else:

			'recepcion'
			try:
				'recv size'
				int_size = __mod__.recv_size( s )
				#print '@cli.recv_size:'.ljust( RJUST ) , int_size
				
				if not int_size:
					raise RuntimeError( 'El servidor no responde' )

				'recv'
				data_obj = __mod__.recv( s , int_size )
				#print '@cli.recv:'.ljust( RJUST ) , repr( data_obj )
				'goto else'

			except: # Exception, e
				
				#msg = '\n[ CLIENT ERROR ]: Error recibiendo el mensaje del servidor. Error e : %s' % e
				#__mod__.raise_exception( msg )

				print '\n[ CLIENT ERROR ]: Error recibiendo el mensaje del servidor ->'
				print  mdl.uber.format_exception()

				#mdl.uber.format_exception( '@Error en cliente en la recepcion de los datos' , e  )			

			else:
				
				if isinstance( data_obj , Exception ): 
					print '\n[ CLIENT ERROR ]: Error recibido desde el servidor ->'
					raise data_obj

				return data_obj

		finally:
			#print 'Cerrando el spcket'
			s.close()

	return client_proxy










########  ######## ##     ##  #######  ######## ######## 
##     ## ##       ###   ### ##     ##    ##    ##       
##     ## ##       #### #### ##     ##    ##    ##       
########  ######   ## ### ## ##     ##    ##    ######   
##   ##   ##       ##     ## ##     ##    ##    ##       
##    ##  ##       ##     ## ##     ##    ##    ##       
##     ## ######## ##     ##  #######     ##    ######## 


class StopRemote( Exception ): pass





class Remote( object ):

	"""
	Remote funciona un poco como ubermodule

	"""

	def __init__( self, module , link=None, cmd=[] ):

		'module'
		self.module = module
		'Se puede utilizar un link temporal @label'
		self.link = mdl.shell( link or ( self.module.__file__ + '.remote' ) )
		'subprocess'
		self.cmd = cmd
	
		'self.proxy y self.address son atributos dinamicos asegurando la buena conexion'
		
		print '+ Remote Instance:' , link , self.link #mdl.uber.debug()

	def __getattr__( self , att ):

		if self.link.ISFILE:
			if att == 'proxy':
				'con esto aseguramos el sp o el thread'
				return __mod__.Client( self.link )
			if att == 'address': 
				return __mod__.read_address( self.link ) 
		else:
			if att in ['proxy','address']: 
				return None

		return object.__getattribute__( self , att  )

	def wait( self , msg = 'waiting ...' , delay = 2 , sleep = 1 ):

		curtm = time.time()
		lapse = getattr( self , '#' , curtm + delay + 1 )
		if ( curtm - lapse ) > delay:
			print msg , time.asctime()
			setattr( self , '#' , curtm )
			
		time.sleep( sleep )



	def loop( self , looper ):
		self.start_worker( looper )	

	def loop_forever( self ,looper ):
		self.start_worker( looper , keep_alive = True )


	def start_worker( self , looper ,  keep_alive = False ): #module = None ,

		'Esta funcion se evalua en el __main__ del thread o del subproceso'
		'El asegurado del servidor lo debe hacer el usuario'

		print '\n%s REMOTE WORKER WAITING FOR TASKS, SIR!\n' % self.module.__name__.upper()
		
		while 1:

			"En cada loop asegura el servidor en un thread"
			'lo pasamos aqui por que como no hay otra forma de asegurar el servidor, no?'
			self.join_server_thread()

			loop_unit = getattr( self.module , looper ) if isinstance( looper , str ) else looper

			try:
				loop_unit( self )
		
			except KeyboardInterrupt:
				sys.exit()
			except:

				if keep_alive:

					print '\n[ERROR] en el remote loop de %s\n' % self.module.__name__
					print mdl.uber.format_exception()
					print '[/ERROR]'
					print '\nArregle el fallo!.Siguiente intento en 5 segundos...\n'
					time.sleep(5)					

				else:

					raise

		print '\n%s REMOTE WORKER DISMISS\n' % self.module.__name__.upper()
		sys.exit()


	def connect( self , attempts = 5 , sleep = 1 , info = '' ):

		'Bloquea moentras intenta conectar al '

		for i in range( attempts ):
			if self.alive():
				return True
			time.sleep( sleep )
		
		err = 'Imposible conectar con el servidor. User info: %s' % info or '< no info provided >'

		#raise mdl.uber.uberException( err  )

		raise RuntimeError, err

	
	def alive( self ):

		link_file_exists = self.link.ISFILE
		proxy_is_online  = bool( self.proxy )

		if link_file_exists and proxy_is_online:
			return True

		return False

	def join_worker_subprocess( self ):

		if not self.alive():
			__mod__.launch_remote_worker_subprocess( self , self.cmd )
			time.sleep(2)

		return self.connect( info = 'Worker creado en un SUBPROCESO' )
		
	def join_worker_thread( self , daemon = True ):

		if not self.alive():
			__mod__.launch_remote_worker_thread( self , daemon )
			time.sleep(.5)
		
		return self.connect( info = 'Worker creado en un THREAD' )


	def join_server_thread( self , daemon = True ):
		
		'Esto debe ser evaluado el el proceso del worker'
		'? como saber si estamos en un worker'

		if not self.alive():
			__mod__.launch_remote_server_thread( self , daemon )
			time.sleep(.5)
		
		return self.connect( info = 'Server creado en un THREAD' )




def launch_remote_worker_subprocess( self , cmd = None ):

	cmd = cmd or self.cmd
	assert cmd
	cmd[0] = mdl.shell( cmd[0] , absolute = True )	 
	sp = subprocess.Popen( cmd )
	print '[ LAUNCHER INFO ]: Creando un worker en un subproceso cmd -> %s' % ' '.join( cmd )
	return sp


def launch_remote_worker_thread( self , daemon = True ):

	def thread():
		fsh = mdl.shell( self.module.__file__ )
		fsh.EVAL

	thr = threading.Thread( None , thread )
	thr.daemon = daemon

	print '[ LAUNCHER INFO ]: Creando un nuevo worker en un thread', self.link , self.module
	thr.start()
	return thr

def launch_remote_server_thread( self , daemon = True ):

	def thread():
		srv = __mod__.Server( self.link , self.module   ) #, self.methods
		srv.start()


	thr = threading.Thread( None , thread )
	thr.daemon = daemon
	
	print '[ LAUNCHER INFO ]: Lanzando un nuevo servidor en un thread', self.link , self.module
	thr.start()
	return thr




########   #######   #######  ##       
##     ## ##     ## ##     ## ##       
##     ## ##     ## ##     ## ##       
########  ##     ## ##     ## ##       
##        ##     ## ##     ## ##       
##        ##     ## ##     ## ##       
##         #######   #######  ######## 


'EJEMPLO PARA LA IMPLEMENTACION DE UN SERVIDOR'




class Pool( object ):
	
	def __init__( self , module ):

		self.mod = module 
		self.sh  = mdl.shell( module.__file__ ).PARENT
		self.pid = os.getpid()
		self.fsh = self.sh( '_%s' % self.pid )

		self.methods = []

		if not self.fsh.ISFILE: self.start_server()
			


	def start_server( self ):
	
		'No hay un servidor creado, creamos uno'	

		def thread():
			print '* POOL server started'
			__mod__.Server( self.fsh , self.mod , self.methods  ).start()

		thr = threading.Thread( None , thread )
		thr.daemon = True
		thr.start()

		


	def validate_fname( self , bn ):

		return bn.startswith('_') and bn[1:].isdigit()


	def local_node( self ):

		fnames = [ bn for bn in self.sh.LIST_FILES if self.validate_fname(bn) and bn == self.fsh.BASENAME ]
		if fnames:
			cli = __mod__.Client( self.fsh )
			return cli
		raise RuntimeError, 'Current process isnt in pool -> %s' % self.sh



















