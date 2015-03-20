
#import re
#import pickle
#import marshal
#import types
#import json
#import socket
#import multiprocessing 
#import multiprocessing.connection as conn

#import traceback


from contextlib import contextmanager
import ast
import hashlib

'''
Necesitamos una estructura leible, por lo tanto implica
que solo los tipos basicos son admisibles 

int float str tuple list dict
'''

########     ###    ########    ###     ######  ########     ###     ######  ######## 
##     ##   ## ##      ##      ## ##   ##    ## ##     ##   ## ##   ##    ## ##       
##     ##  ##   ##     ##     ##   ##  ##       ##     ##  ##   ##  ##       ##       
##     ## ##     ##    ##    ##     ##  ######  ########  ##     ## ##       ######   
##     ## #########    ##    #########       ## ##        ######### ##       ##       
##     ## ##     ##    ##    ##     ## ##    ## ##        ##     ## ##    ## ##       
########  ##     ##    ##    ##     ##  ######  ##        ##     ##  ######  ######## 

import mdl
__mod__ = mdl.uber.uberModule()



class DataSpace( dict ):


	def __init__( self, path , load = True ):

		self.__file__  = mdl.shell( path , delegated = True )
		
		self.__checksum__ = None

		if not self.__file__.EXISTS:
			self.dump()		

		if load:
			self.load()


	def loads(self,s):
		
		data = __mod__.decode( s )
		self.update( data )
		return data

	def checksum( self ):

		return hashlib.md5( self.dumps() ).hexdigest() 


	def src_changed( self ):

		src_checksum = hashlib.md5( self.__file__.READ ).hexdigest()
		return False if self.checksum() == src_checksum else True


	def mem_changed( self , use_src = False ):
		
		return False if self.checksum() == self.__checksum__ else True

	def dumps( self ):

		return __mod__.encode( self.copy() )

	def load(self):

		with self.__file__.R as f:
			code = f.read()

		data = __mod__.decode( code  )

		self.clear()
		self.update( data )

		self.__checksum__ = self.checksum() #hashlib.md5( code ).hexdigest()
		
		return self

	def dump(self):

		data = self.dumps()
		
		with self.__file__.W as f:
			
			f.write( data )
			mdl.log.debug( '@dspace dumped: %s\n' % self.__file__)

		self.__checksum__ = self.checksum()
	
		return self

	@contextmanager
	def lock( self ):
		with self.__file__.LOCK:
			with self:
				yield self
		
			
	def __enter__( self ):

		#print '\t\t__enter__ dspace'
		self.load()
		return self

	def __exit__( self , *err ):
		
		if any( err ):
			mdl.log.debug( 'Error con el proceso con el dataspace, datos no guardados' )
			return

		self.dump()
		#print '\t\t__exit__ dspace'


#	@contextmanager	
#	def lock(self):
#		with self.__file__.LOCK:
#			with self:
#				yield self
#
#	@contextmanager	
#	def netlock(self):
#		with self.__file__.NETLOCK:
#			with self:
#				yield self			

#	def __enter__( self ):
#		
#		with self.__file__.LOCK:
#			self.load()
#			print '\t\t__enter__ dspace'
#			return self
#
#	def __exit__( self , *err ):
#		
#		if any( err ):
#			mdl.log.debug( 'Error con el proceso con el dataspace, datos no guardados' )
#			return
#		'dump if no errors'
#		#print 'DUMPED dataspace '
#		self.dump()
#		print '\t\t__exit__ dspace'
#

	def __repr__( self ):

		return self.dumps()

	def __str__( self ):

		return repr( dict( self ) )






######## ##    ##  ######   #######  ########  ######## ########   ######  
##       ###   ## ##    ## ##     ## ##     ## ##       ##     ## ##    ## 
##       ####  ## ##       ##     ## ##     ## ##       ##     ## ##       
######   ## ## ## ##       ##     ## ##     ## ######   ########   ######  
##       ##  #### ##       ##     ## ##     ## ##       ##   ##         ## 
##       ##   ### ##    ## ##     ## ##     ## ##       ##    ##  ##    ## 
######## ##    ##  ######   #######  ########  ######## ##     ##  ######  


def validate( value ):

	try:
		ast.literal_eval( repr( value ) )
		#marshal.dumps( value )
	except:
		#traceback.print_exc()
		return False
	else:
		return True



def encode( obj , parents = [] , done = [] , validate = '???' ):

	assert isinstance( obj , dict ) , 'dict only'

	done = done or [ obj ]

	result = ''	
	tabs = '\t'*len(parents)	
	
	if tabs:
		result += tabs[:-1] + parents[-1][0] + ':\n'

	for k,v in sorted( obj.iteritems() ):

		if isinstance( v , dict ):
			
			parents.append( (k,v) )
			done.append( v )
			result += __mod__.encode(  v , parents , done )
			parents.pop()	

		elif isinstance( v,(list,tuple)):

			codes = [ item for item in v if __mod__.validate( item )]
			result += tabs + "%s: %s\n" % ( k , repr(codes) )

		else:
			if __mod__.validate( v ):
				result += tabs + "%s: %s\n" % ( k , repr(v) )		

	return result


def decode( code ):

	indent = lambda s: len(s)-len(s.lstrip())

	lines = [ ( indent(l) , l ) for l in code.split('\n') if l.strip() ]

	roots = [ {} ]

	for idx ,line in lines:

		diff = ( idx + 1 ) - len( roots )
		while diff < 0:
			roots.pop()
			diff += 1

		part = line.partition( ':' )
		label = part[0].strip()
		
		#try:
		#	label = ast.literal_eval( label )
		#except:
		#	raise mdl.uber.uberException()

		code = part[-1].strip()

		target = roots[-1]	

		if code:

			target[label] = ast.literal_eval( code ) #eval(code)

		else: # no code new structure

			new = target.setdefault( label , {} )
			roots.append( new )			

	return roots[0]







 ######  ########  ######   ######  ####  #######  ##    ## 
##    ## ##       ##    ## ##    ##  ##  ##     ## ###   ## 
##       ##       ##       ##        ##  ##     ## ####  ## 
 ######  ######    ######   ######   ##  ##     ## ## ## ## 
      ## ##             ##       ##  ##  ##     ## ##  #### 
##    ## ##       ##    ## ##    ##  ##  ##     ## ##   ### 
 ######  ########  ######   ######  ####  #######  ##    ## 



class Session(object):

	def __init__( self, *args , **kwargs ):
		d = dict( *args , **kwargs )
		self.__dict__.update( d )

	def __call__( self , key , default ):
		return self.__dict__.setdefault( key , default )

	def __getitem__( self , k ):
		return getattr( self , k )

	def __setitem__( self, k , v ):
		setattr( k , v )



