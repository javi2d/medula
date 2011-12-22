#!/usr/bin/env python
# encoding: utf-8

"""
sop.py

Space Oriented Programming, Python Implemementation.

Created by Javier Garcia on 2010-07-13.
Copyright (c) 2010 Javier Garcia. All rights reserved.

"""


#print 'THIS SOP MODULE HAS A QUEUE IMPLEMENTATION OF SPACES RESOLUTION'

import sys
import time
import os

if __name__ == '__main__':

	print '\nSop Module Cannot be Executed Directly'
		
	sys.exit()


import __main__ as main

main.main = main

sop = sys.modules[ __name__ ] # reemplzar por __name__????  'sop'




class Normalize:
	

	
	@staticmethod
	def name( name ):
		
		import string
		
		'''
		return normalized name aA-zZ , 0-9 , _
		
		'''
		
		
		normalized = ''

		for char in name:
			
			if char.isdigit() or char in string.ascii_letters:
			
				normalized += char
				
			else:
				
				normalized += '_'
						

		if normalized and normalized[0].isdigit():

			normalized = '_' + normalized

		return normalized

	@staticmethod
	def dirname( path_string ):

		return Normalize.path( os.path.dirname( path_string ) )
		
		
	
	@staticmethod
	def path( path_string ):
		
		'''
		return normalized path
		
		'''
		
		
		if path_string == '' :
			
			return ''
		
		elif type( path_string ).__name__ in ['str','unicode']:
			
			normalized = os.path.normpath( path_string )
			
			normalized = os.path.expandvars( normalized )
			
			normalized = normalized.replace( '\\' , '/' ).strip()
			
			normalized = normalized.replace( r'\\' , '/' ).strip()
			
			#normalized = normalized.replace( '//' , '/' ).strip()
			
			if normalized.endswith('/'):
				
				normalized = normalized[:-1]
			
			
			return normalized
		
		else:
			
			raise AttributeError( '\n\nERROR : sop.Normalize.path need string as arg !!\n\n' )


	@staticmethod
	def split( path ):
		
		path = Normalize.path( path )
		
		dirname , basename = os.path.split( path )
		name , ext = os.path.splitext( basename )
		
		return dirname , basename , name , ext 

	@staticmethod
	def walk( path ):
		
		for P,D,F in os.walk( path ):
			
			P = Normalize.path( P )
			
			yield P,D,F
			


		
	@staticmethod
	def join( *args ):
		
		'''
		same as os.path.join but with multiple arguments, result is Normalized
		
		'''
		
		
		path = ''

		for item in args:

			if type( item ).__name__ == 'Shell':

				item = item['$PATH']
		
			#item = os.path.normalize( item )
		
			if ':' in item:
			
				path = item
			
			else:
				
				if path.endswith(':'):
					
					path += '/'
				
				path = os.path.join( path , item )
				
		return Normalize.path( path )
	
	
		
	
	
	@staticmethod
	def code( code_string , end_error = True ):
		
		'''
		return normalized code_string , fixes endlines.
		
		'''
		
		
		code_string = code_string.replace( '\r\n' , '\n')
		code_string += '\n'
		
		if end_error:
		
			code_string += '\npass # ERROR : Check closure of last code structure\n'
		
		return code_string


	@staticmethod
	def shell( shell_or_path ):
    
		if type( shell_or_path ).__name__ == 'Shell':
    
			shell = shell_or_path
			
		elif type( shell_or_path ).__name__ == 'Space':
			
			raise RuntimeError( 'Space passed to Normalize.shell' )
    
		else:
    		
			shell = Shell( shell_or_path )
    
		return shell
	
		
	@staticmethod
	def space( space_or_path ):	
		
		if type( space_or_path ).__name__ == 'Space':
    		
			if space_or_path['file']:
			
				path = space_or_path['file']
			
			else:
				
				raise RuntimeError( 'Not monofile Space passed to Normalize.space' )
			
		elif type( space_or_path ).__name__ == 'Shell':
			
			raise RuntimeError( 'Shell passed to Normalize.space' )
    
		else:
    		
			path = space_or_path
    	
		return path
		
		
	




class Expose:

	@staticmethod
	def object( obj , label  ):

		'''
		Expose obj as label into main and sop, making obj widely available

		'''
		
		if label == 'brain':    # Not exposed

			if not hasattr( main, label ):

				setattr( main , label , obj )

			if not hasattr( sop, label ):	

				setattr( sop , label , obj )
		

		else:

			setattr( main , label , obj )

			setattr( sop , label , obj )
			
			#print sop == main.sop
		
		return obj
		


	@staticmethod
	def modules( modules ):
		
		'''
		Expose modules into main and sop, making modules widely available
		modules arg is in form "sys os string"
		
		from mod import * is not implemented
		
		
		'''
		
		
		for name in modules.split(' '):

			if name:

				name = name.strip()

				try:

					module = __import__( name )
					Expose.object(  module , name  )

				except ImportError:

					print '!!WARNING. Error importing [ %s ] Module ' % name

	

	@staticmethod				
	def folder( shell_or_path , into = '' , recursive = False , marshalize = False ):
	
	# Deprecated by Brain << shell
		
		
		shell = Normalize.shell( shell_or_path )

		if recursive:

			shell = shell._	

		base_index = len( os.path.dirname( shell['$PATH'] ) ) + 1

		print '\n>>Exposing Folder : %s\n' % shell['$PATH'] 

		for item_name in shell['$DIR']:

			item_space = getattr( shell , item_name )

			if type( item_space ).__name__ == 'Shell':

				item_space = item_space['$SPACE']

			if marshalize:

				item_space.__marshalize__()

			route = item_space['shell']['$PATH'][ base_index: ].replace( '/' , '.' )
			
			
			route = '.'.join( [ into , route ] )
			
			
			setattr( main.brain( route , Brain() ) , item_space['name'] , item_space() )

			# memory loaded item info

			print '     >> INFO brain.%s.%s << %s' % ( route , item_space['name'] , [ os.path.basename(p) for p in item_space['files'] ]  )


		print





class Core:
	
	__interpreter__ = None
	
	__stdout__ = None
	
	#__domains__ = [  ] 
	
	@staticmethod
	def output_redirect( path = None ):
		
		Core.__stdout__ = sys.stdout
		
		if path:
		
			sys.stdout = open( path , 'w' )
	
		else:
			
			sys.stdout = sys.__stdout__
		
		
	@staticmethod
	def output_restore():
		
		if not Core.__stdout__:
			
			raise RuntimeError( 'Cannot Restore Output' )
		
		if not sys.stdout == sys.__stdout__:	
			
			sys.stdout.close()
		
		sys.stdout = Core.__stdout__
		Core.__stdout__ = None
	
	
	#@staticmethod
	#def add_domain( path ):
	#	
	#	if path not in Core.__domains__:
	#		
	#		Core.__domains__.append(  Normalize.path( path )  )
	#
	#
	#		
	#@staticmethod
	#def remove_domain( path ):
    #
	#	if path in Core.__domains__:
    #
	#		Core.__domains__.remove( path )
	#
	#		
	#@staticmethod
	#def in_domain( path ):
	#	
	#	path = Normalize.path( path )
    #
	#	matches = [ x for x in Core.__domains__ if path.startswith( x ) ]
	#	
	#	print '???' , path
	#	print matches
	#	
	#	return True if matches else False
				
			
	
	
	@staticmethod
	def thread( fun , *args , **kwargs  ):
		
		import threading
		return threading.Thread( None ,  fun , args = args , kwargs = kwargs )
	

	
	@staticmethod
	def date( ):
			
		return '_'.join( [ '%02d' % x for x in time.localtime()[:3] ] )
		

	@staticmethod
	def time():
		
		return '_'.join( [ str(x) for x in time.localtime()[3:6] ] )
	
	@staticmethod
	def lap( route ):
		
		now = time.time()
		
		if not route:
			
			raise AttributeError( '\nbrain.lapses route needed' )
		
		
		elif route == '.':
			
			print '\nPublic Lapses : ',
			
			print brain.lapses.public


		elif route == '_':
			
			print '\nPrivate Lapses : ',
			
			print brain.lapses.private
		
		
		elif route.startswith('//'):
			
			route = route[2:]
			
			b = ( brain.lapses.private 	if route.startswith( '_' ) else brain.lapses.public	)
			
			Core.lap( '/' + route )
			
			lapses = [ float( x ) for x in b( route , [] ) ]

			b( route , [ '%.4f' % ( sum( lapses ) / len( lapses ) ) ] , replace_att = True ) 
			

			
		elif route.startswith('.//'):
	
			route = route[3:]
			 
			b = ( brain.lapses.private 	if route.startswith( '_' ) else brain.lapses.public	)
			
			Core.lap( '/' + route )
			
			lapses = [ float( x ) for x in b( route , [] ) ]

			current_lapses = [ '%.4f' % ( sum( lapses ) / len( lapses ) ) ]
				
			print '\nAveraged Lapses for "%s" tag : %s\n' % ( route , current_lapses )
			
				
			
		elif route.startswith('./'):
			
			route = route[2:]

			Core.lap( '/' + route )
			Core.lap( '.' + route )
		
			
		elif route.startswith(':'):
			
			route = route[1:]
			b = ( brain.lapses.private 	if route.startswith( '_' ) else brain.lapses.public	)	
			b( route , [] )[:] = []
			
		
		elif route.startswith('.'):
		# Print laps for tag
		
			route = route[1:]
			b = ( brain.lapses.private 	if route.startswith( '_' ) else brain.lapses.public	)	
			
			print '\nLapses for "%s" tag :\n %s\n' % ( route , b( route ) )
			
		
		elif route.startswith('/'):
		# Ends and Write lapse for tag
			
			route = route[1:]
			
			b = ( brain.lapses.private 	if route.startswith( '_' ) else brain.lapses.public	)	
			
			lap = brain.lapses._laps( route , None  )
			
			if lap:
			
				b( route , [] ).insert( 0 , '%.4f' % ( now - lap ) ) #
				
				brain.lapses._laps( route , None , replace_att = True )
			
			
			
	
		else:
		# Time mark for tag
		
			brain.lapses._laps( route , now , replace_att = True )

	
	@staticmethod
	def softReload():
		
		reload( main.sop )
		
	
	#@staticmethod
	#def hardReload():
	#	
	#	#del main.sh
	#	del main.brain
	#	del main.this
	#	
	#	reload( main.sop )
	
	

	@staticmethod
	def eval( code , space = main , tag = None ):
		
		'''
		
		Evaluates code string over space
		
		'''
		
		tag = '< code string evaluation :: %s  >' % repr( tag )
		
		
		
		__code__ = Normalize.code( code  )
		
		import code
		
		interpreter = code.InteractiveInterpreter( vars( space ) )
		
		interpreter.runsource( __code__  , tag , 'exec')
		
		
		return space
		
	
	@staticmethod
	def execution( path , space = None , **kwargs): 
		
		# Execute path file over space

		path = Normalize.path( path )

		if not space:
			space = Space( [ path ] )

		else:
			space.space = space

		dirname, basename, name, ext = Normalize.split( path )
		
		
		
		
		
		# start lapse 
		
		lapse_tag = 'sop.Core.execution.%s' % basename
		Core.lap( lapse_tag )
				
		
		
		current_cwd = os.getcwd()		
		
		os.chdir( dirname )
		
		for k,v in kwargs.items():

			setattr( space, k, v)

		
		
		try:
		
			if ext in ['.pyc','.pyo']:

				print '\n!WARNING : Use of compiled python code files ( pyc ) is discouraged and partially suported, use marshal code instead.\n'	

				sys.path.append( dirname )

				idx = len( sys.path ) - 1 

				if name in sys.modules:

					m = sys.modules[ name ]

					reload( m )

				else:

					m = __import__(name)

				for k,v in vars( m ).iteritems():

					setattr( space, k, v )

				#space.__file__ = path

				sys.path.pop( idx )


			elif ext == '.marshal':


				import marshal

				source = open( path , 'rb')	

				code_object = marshal.load( source )

				import code

				interpreter = code.InteractiveInterpreter( vars( space ) )
				interpreter.runcode( code_object )



			else:
			
				import code

				f = open( path )

				__code__ = f.read()	

				f.close()

				if __code__:

					__code__ = Normalize.code( __code__ )
					
					interpreter = code.InteractiveInterpreter( vars( space ) )
					
					Core.__interpreter__ = interpreter
					
					code_object = code.compile_command( __code__ , 'sop.Space >> %s' % path , 'exec' )

					interpreter.runcode( code_object )
						
					#interpreter.runsource( __code__  , 'sop.Space >> %s' % path , 'exec') #os.path.basename(path)
							
					
		except:
	
			raise 	
			
		finally:
			
			os.chdir( current_cwd )
		
		
		# close the lapse 
		Core.lap( '/%s' % lapse_tag  )
		
		
		if type(space).__name__ == 'Space' and space['file']:
			
			_ , basename = os.path.split( space['file'] )
			
			space.__called__ = True

			Space.__spaces__['unlock']

			Space.__spaces__( basename , space , replace_att = True )

			Space.__spaces__['lock']


		return space


	
	
	@staticmethod
	def marshalize( path_or_space ):
		
		'''
		Marshalize provided path or space, only py files can be marshalized

		'''
		
		if type( path_or_space ).__name__ == 'Space':
			
			path = path_or_space['exts'].get( '.py' , None )
			
			if not path:
				
				raise ValueError( 'there is no .py file in space, cannot be marshalized' )

		else:

			path = path_or_space


		if path:

			import code
			import marshal

			path = Normalize.path( path )

			dirname, basename = os.path.split(path)
			name, ext = os.path.splitext( basename )

			f = open(path)

			codeString  = f.read()

			if codeString:

				codeString = Normalize.code( codeString )

				basename = os.path.basename( path )

				co = code.compile_command( codeString , '<%s>' % basename , 'exec' )

				solver_path = os.path.splitext( path )[0] + '.marshal'

				solver_path = Normalize.path( solver_path )

				target = open( solver_path , 'wb' )

				marshal.dump( co, target )

				target.close()

				print '>> %s file has been Marshalized' % basename








class Void(object):
	
	def __init__( self , clue = None ):
		
		self.__clue__ = repr( clue )
		
		raise AttributeError( '\n\nERROR ! Void __init__ error. PASSED_ARG =  %s' %  self.__clue__  )	

	def __getattr__( self, att ):
		
		raise AttributeError( '\n\nERROR ! Void __getattr__ error. ATT = %s  CLUE =  %s' % ( att , self.__clue__ )  )
	
	def __setattr__( self, att ,value ):
		
		if not att == '__clue__' and '__clue__' in dir( self ):
		
			raise AttributeError( '\n\nERROR ! Void __setattr__ error. ATT = %s VALUE = %s  CLUE =  %s' % ( att , repr(value) , self.__clue__ )  )
		
		else:
		
			super( Void , self ).__setattr__( att , value )
	
	def __nonzero__( self ):

		return False

	
	

class Brain(object):
	

	def __init__( self , logical = False ): #content = None , 
		
		#if content:
		#
		#	for n,v in  
		
			
		self.__lock__ = False
		
		self.__names__ = []
		
		self.__logical__ = logical
		
	
	def __call__(self , att_route = Void , default_value = Void , create_att = True , replace_att = False ):

		''' 
		Brain( 'route.to.attribute' ,  ) 
		
		'''		
				
		# filtering att route
		
		if type( att_route ).__name__ not in ['str','unicode']:
			
			raise AttributeError( '\n\nBrain.__call__() first arg must be string, current is :: %s\nBrain routes are : %s' % ( repr( att_route ) , self['routes'] )  )
		
		elif default_value == Void:
			
			# if no default value defined , every item of attrib route must exist 

			atts = [ att for att in att_route.split('.') if att ]
			
			current = self 
			
			while atts:
				
				att = atts.pop(0)
				
				if att in current.__dict__:
	
					current = getattr( current , att )
				
				else:
					
					raise AttributeError( '\nERROR ! Unexistent att in brain ( Void )\n\n    brain routes = %s\n    att_route = "%s".\n    invalid att = "%s".\n\n' % ( self['routes'] , att_route , att ) )
			
			
			return current
			
			
		else:
			
			atts = [ att for att in att_route.split('.') if att ]

			current = self

			while atts:

				att = atts.pop(0)
				
				if not atts:    # last item

					if att in dir( current ): # attribute exists
					
						if replace_att:

							if default_value == Void:

								default_value = default_value( att_route )
							
							setattr( current , att , default_value ) 
							
						current = getattr( current , att )
	
					else:  # attribute not exists
												
						if create_att:
							
							if default_value == Void:

								default_value = default_value( att_route )
							
							setattr( current , att, default_value )
							
							current = getattr( current , att )
							
						else:
							
							if default_value == Void:
							
								raise AttributeError( 'att [ %s ] not found in [ %s ]' % ( att , repr( current ) ) )
							
							current = default_value
								
				
				else:			# intermediate Items
				
					current = getattr( current , att ) # Brain if undefined
				
			return current
	
	
	def __lshift__(self, other):
		
		
		def filter_type( self, name, value  ):
			
			value_type = type(value).__name__

			if value_type in [ 'Space' , 'classobj' , 'Brain']:
						
				self( name , Brain() ) << value
					
			else:
				
				self.__dict__[ name ] = value
				

		
		
		if type(other).__name__ == 'Shell':
			
				
			base_index = len( other['$PATH'] ) + 1

			print '\n( brain << shell ) %s\n' % other['$PATH']  #'#Injecting Folder : %s\n' % other['$PATH'] 
			
			for relpath in other['$DIR']:
				
				dirname , name = os.path.split( relpath )
									
				space = getattr( other( dirname ) , name )
				
				route = relpath.replace( '/' , '.' )
												
				self( route , space() , replace_att = True )
	
				print '     >> INFO brain.%s << %s' % ( route , relpath )

			print
			
	
		elif type(other).__name__ == 'Space':
	
			if not other[ 'called' ]:
				
				if not other[ 'file' ]:
					
					raise IOError( 'ERROR 1 in brain << other non monofile space , files : %s ' % other['files'] )
					
				else:

					exts = []

					for solver in Solver.__solvers__:
					
						exts.extend( solver() )
					
					dirname , basename , name , ext = Normalize.split( other[ 'file' ] )
					
					if ext in exts:
						
						other = other()
					
					else:
						
						other = other['exec'] # for example a .memory file will not resolve, so you need to Execute manually	
					
			
			for name in other['user_data']:
				
				#print '>>' , name
				
				value = other.__dict__[ name ]
				
				if value == other: # this happens when space itself is passed to itself 
					
					self.__dict__[ name ] = value
				
				else:
					
					filter_type( self, name,  value )
					
					

				
		
		elif type(other).__name__ == 'classobj':
			
			for name in [ n for n in dir( other ) if not n.startswith( '__' ) ]: #if n[0] != '_' ]:
				
				#print '*' , name
				
				filter_type( self, name, getattr( other, name )  )
					
		
		elif type(other).__name__ == 'Brain':
			
			for name, value in other['items']:

				filter_type( self, name, value )
				
		
					
		return self		
	
	

	__rshift_ERROR1__ = 	'''

Error description on operation brain >> space

Brains content can be dumped into a file defined by an space. 

If this error appear, your right object is not an Space type.

		'''
	
	__rshift_ERROR2__ = 	'''

Error description on operation brain >> space

You need a monofile space

Clues:

space['files'] = %s

			'''


	
					
	
	def __rshift__(self, other ):
		
		other_type = type(other).__name__
		
		
		if not other_type == 'Space':
			
			raise IOError( Brain.__rshift_ERROR1__ )
			
		# other is a Space
		
		if not other['file']:
			
			raise IOError( Brain.__rshift_ERROR2__  % other['files'] )
		
		# other is a monofile Space
		
		# @ Removed support to other file extensions. Brains can only be dumped onto .memory or .log files
		
		memo_file =  other['file']
		
		#if memo_file and not Core.in_domain( memo_file ):
		#	
		#	raise RuntimeError( '\nBrain out of DOMAIN :: %s\n\nAvailables domains are >> %s\n' % ( memo_file , Core.__domains__ ) )
		
		
		
		
		dirname, basename , name , ext = Normalize.split( memo_file )
		
		if ext not in ['.log' , '.memory' ]:
			
			raise IOError( 'Use .log or .memory to dump brains.' )
		
		
		if ext == '.log':
			
			log_file = target_file
			
			memo_file = Normalize.join( dirname , name + '.memory' )
			
			f = open( memo_file )
			
			memory = f.read()
			
			f.close()
			
			h = open( log_file , 'a' )
			
			separator_line = '\n\n# < AUTOSAVED HISTORY  %s-%s-%s  %s:%s.%s >\n\n' % time.localtime()[:6]

			h.write( separator_line + memory )

			h.close()
		

		# Overwrite .memory file
		
		lock_file = Normalize.join( dirname , name + '.lock' )
		
		new_code = self.__code__()
		
		tries = 10
		
		while os.path.isfile( lock_file ):
		
			print '\nWaiting for file unlock : %s.lock \n' %  name ,
			
			tries -= 1
		
			if not tries:
				
				raise IOError( 'Please revise and manually delete file: %s .' % lock_file )
				
			time.sleep(.1)
		
			
			
		f = open( lock_file , 'w' )
		
		try:
		
			f.write( new_code  )  #Normalize.code( ''.join( new_code ) , end_error = False )  pasado a __code__
		
		except:
			
			print '\nWarning Error writing .lock file : %s ' % lock_file
			
		finally:
		
			f.close()
		
			import shutil
		
			shutil.move( lock_file , memo_file )

			#print '\nbrain >> %s ' %  memo_file[-50:]


		return self
		
		
		
			
			
			
			
	
			
			
			
	
	
	def __code__( self ):
		
		""" 
		
		Generates code from brain structure
		
		
		"""

		CODE = []
		
		
		
		to_analize = [ ( None, self, 0 ) ]
		
		
		
		while to_analize:

			name , obj , level = to_analize.pop()
			
			if name:
				
				tab_level = '\t' * (level-1)
				
				CODE.append( '\n%sclass %s:\n\n' % (tab_level , name) )
			
			names = [ x for x in dir(obj) if not x.startswith( '__' ) ] #x[0] != '_' ]
				
			tab_level = '\t' * (level)
			
			if not names:
				
				CODE.append( '%spass\n' % ( tab_level ,)  )
				
				continue
			
			for name in names:
				
				value = obj.__dict__[ name ]
				
				value_type = type(value).__name__
				
				if value_type in ['classobj' , 'Brain' ]:
					
					to_analize.append( ( name , value , level+1 ) )
				
				# Las funciones se podrian dumpear con objetos code marshalizados, pero es ilegible, 
				# brain >> space  queda restringido a valores legibles.
				
								
				else:
					
					try:
						
						if eval( repr( value ) ) == value:
							
							code_line = '\n%s%s = %s\n'
							
							if tab_level:
								code_line = '%s%s = %s\n'
							
							CODE.append( code_line % ( tab_level , name , repr( value ) ) )	
						
					
					except:
							
						raise RuntimeError('''
						
Error description on operation brain.__code__

	Your Brain structure contains values that not match
	
		eval( repr( value ) ) != value
	
	Clues:
		
		att_name = %s
	
		repr( value ) = %s
	
						
						''' % ( name , repr( value ) )  )
		

		return Normalize.code( ''.join( CODE ) , end_error = False )
	
	
	
	
	
	def __setattr__( self , att , value ):
		
		'''
		wrapper to resort att in self.__names__ 
		
		'''
		
		if  att.startswith( '__' ) and att.endswith( '__' ):
			
			object.__setattr__( self , att , value)
			
		else:

			if self.__lock__:
			
				#return Void(  )
			
				raise AttributeError , '\nbrain "locked" __setattr__  BRAIN ROUTES : %s  ATT : %s VALUE : %s' % ( self['routes'] , att , value )
		
		
			elif not att.startswith('__'):
			
				self.__names__[:] = [ n for n in self.__names__ if not att == n ] + [ att ]
			
			
			object.__setattr__( self , att , value)
		
		
		#super( Brain , self ).__setattr__( att, value )
		
	
	def __getattr__(self, att):
		
		'''
		We are getting an attribute that not exists in Brain
		
		'''
		
		if att.startswith( '__' ) and att.endswith( '__' ):
			
			pass #super( Brain , self ).__getattr__( att )
		
		elif self.__lock__:
			
			#return Void(  )
			
			raise AttributeError , '\nBrain is locked : BRAIN ROUTES : %s  ATT : %s ' % ( self['routes'] , att )
		
		else:
						
			newBrain = Brain()
			
			setattr( self, att, newBrain )
		
			return newBrain
	
	

			
	
	def __walk__(self, level = 0 , print_value = True ):

		return_string = ''
		
		if level == 0:
			
			main._tmp_brain_walk_done = [ self ]
			
		for att in [x for x in dir(self) if not x.startswith('__') ]: #x[0] not in ['_']

			item = getattr(self,att)
		
			if type(item).__name__ == 'Brain':
				
				if item in main._tmp_brain_walk_done:
					
					return_string += ''
				
				else:
					
					return_string += '\n\n' + '\t'*(level)
				
					return_string += '[b] [ %s ]:\n' % att
				
					return_string += item.__walk__(level + 1, print_value )
				
					main._tmp_brain_walk_done.append( item )
				
			else: 
				
				if level:
					
					return_string += '\n'
					
				else:
					
					return_string += '\n\n'
				
				
				return_string += '\t'*(level-1 if level else 0 ) + ('\t' if level else '')
				
				return_string += '[v] %s' % ( att, ) 
			
				if print_value:
					
					return_string += ': %s%s' %  ( repr( item )[:80] , ('...' if  len( repr( item ) ) > 80 else ''  )  )
			
				else:
				
					return_string += ': ---' 
		
		if level == 0:
				
			del main._tmp_brain_walk_done
		
			return_string = '\n'.join( [ '    '+line for line in return_string.split('\n') ] )
		
			if self['routes']:
		
				title = '\n[b] %s' % self['routes']
		
			else:
				
				title = '\n[b] Anonymous Brain'
		
			return title + return_string + '\n\n'
		
		
		return return_string.replace( '\t' , '    ' )
	
	
	
	
	def __str__( self ):
		
		return self.__walk__()
	
	
	
	def __routes__( self , all_routes = False ):
		
		
		routes = []
		
		brains = []
		
		for k,v in vars( main ).items():
				
			if not v == self and type( v ).__name__ == 'Brain':
				
				brains.append( ( k,v ) )
		
		
		done  = []
		
		route = ''
		
		while brains:
			
			name , brain = brains.pop(0)
			
			brain_atts = [ (l,v) for l,v in brain['items'] if type( v ).__name__ == 'Brain' and v not in done ]
			
			for label , value in  brain_atts:
				
				route = '%s.%s' % ( name , label )
				
				#print route
				
				if type( value ).__name__ == 'Brain':
					
					if value == self:
						
						routes.append( route )
					
					elif value not in done:
					
						brains.append( ( route  , value ) )
		
		
		routes = routes or [ k for k,v in vars( main ).items() if self == v ]
			
		return routes
	
	
	
		
	def __getitem__(self, query ):
		
		# poner token variables
		# hacer un query por variable name brain['my_var'] return a concidence list of that var
		
		
		if False:
			pass
		
		elif query == 'code':
			
			return self.__code__()
			
		elif query == 'routes':
			
			return self.__routes__()
			
			
		elif query == 'parents':
			
			parents = []

			for route in self['routes']:
				
				route = route.split('.')
				
				base_brain = getattr( main , route.pop(0) )
				
				parent_route = '.'.join( route[:-1] )
				
				if parent_route:
				
					parents.append(  base_brain( parent_route ) )
					
				else:
					
					parents.append( main )	
				

			return parents
			
		elif query == 'route_parent':
			
			return zip( self['routes'] , self['parents']  )
	
		
		
		elif query == 'names':
			
			return [ x for x in dir(self) if not x.startswith( '__' ) ] #x[0] not in ['_'] ]
		
		elif query == 'public_names':
			
			return [ x for x in dir(self) if not x.startswith( '_' ) ] #x[0] not in ['_'] ]

		elif query == 'private_names':
			
			return [ x for x in dir(self) if x.startswith( '_' ) and not x.startswith( '__' ) ] #x[0] not in ['_'] ]
	
	
		
		elif query == 'values':
			
			names = self['names']
			
			return [ getattr( self, name )  for name in names ]
			
		elif query == 'public_values':
			
			names = self['public_names']
			
			return [ getattr( self, name )  for name in names ]
		
		elif query == 'private_values':
			
			names = self['private_names']
			
			return [ getattr( self, name )  for name in names ]
	
	
	
		elif query == 'items':
			
			return zip( self['names']  , self['values'] )
			
		elif query == 'public_items':
			
			return zip( self['public_names']  , self['public_values'] )
		
		elif query == 'private_items':
			
			return zip( self['private_names']  , self['private_values'] )	
		
	
				
		elif query == 'dict':
				
			return dict( self['items'] )
		
		elif query == 'public_dict':
				
			return dict( self['public_items'] )
		
		elif query == 'private_dict':
				
			return dict( self['private_items'] )
	
	
			
		elif query == 'lock':
				
			self.__lock__ = True
			
			return self
		
		elif query == 'unlock':
				
			self.__lock__ = False
								
			return self
		
		else:
			
			raise AttributeError( 'Query [ "%s" ] not found in brain' % query )
		



	

class Space(object):

	'''
	Creates a clean execution space
	
	a Space needs to know its parent shell
	
	'''
	
	__spaces__ = Brain()
	
	__chain__ = []

	def __new__(cls, files = [ ] ):
		
		files = [ Normalize.path( f ) for f in files ]
		
		#if files and not Core.in_domain( files[0] ):
		#	
		#	raise RuntimeError( '\nSpace out of DOMAIN :: %s\n\nAvailables domains are >> %s\n' % ( files[0] , Core.__domains__ ) )
		
		
		self = super(Space, cls).__new__(cls)
		
		self.__files__  = files
		
		self.__file__   = ( files[0] if len(files)==1 else None )
		
		self.space      = self
		
		self << sop
		
		self.__called__ = False
		
		self.__proto__ =  sorted( self.__dict__.copy().items() )    # copia de las variables del espacio recien creado
		
		self.__proto__.append( ( '__proto__' , self.__proto__ ) )
		
		
		return self
	
	
	
	def __call__( self , *args , **kwargs ):
		
	
		# Called Space, Double call
		
		Space.__chain__.append( self )
		
		
		if self[ 'called' ]: 
			
			import operator
			
			name = self['name']
			
			auto_called = getattr( self, name , None )
			
			if auto_called:
			
				if operator.isCallable( auto_called ): # deprecated   use  isinstance(x, collections.Callable)
				
					return auto_called( *args ,**kwargs )
				
				else:
					
					raise AttributeError( '\nSpace Double call attribute error:\nvar [ %s ] in space ( %s ) is not callable.\n' % ( name, name )  )
	
			else:
				
				raise AttributeError( '\nSpace Double call attribute error:\nvar [ %s ] not exists in space ( %s ).\n' % ( name, name )  )
		
		
		# Uncalled Space

		else:  
			
			if kwargs:
			
				for k,v in kwargs.items():

					setattr( self , k ,v )
			
			
			solvers = [] 
						
			
			# Redefined args
			
			for arg in args:
			
				if type( arg ).__name__ == 'Space':
					
					self << arg
					
				elif type( arg ).__name__ in ( 'str' , 'unicode' ):
					
					# args are in form ['.py' , '.panel' ]
					
					for solver in Solver.__solvers__:
						
						if arg in solver():
							
							solvers.append( solver )
			
			solvers = solvers or Solver.__solvers__[:] # Maybe a solver could be defined in space call
			
			# A not solvable file will not be solved through space call
	
			for solver in solvers:
		
				solver( self )
						
		
			self.__called__ = True			
			
			if Space.__chain__ : Space.__chain__.pop()
			
			
			return self
			
			
			
	
	def __recall__( self ):
		
		print '\n\nRECALL is highly experimental \n\n'
					
		if self[ 'called' ] and self[ 'files' ]:
			
			for solver in Solver.__solvers__[:]:
				
				solver( self )
			
			return self
			
			
		else:
			
			if not self['called']:
			
				raise ValueError("A not called space cannot be recalled, initialize it." )
			
			elif not self['files']:
				
				raise ValueError("An empty space cannot be recalled." )
				
			else:
				
				raise ValueError("Space Recall unknown error." )
		
				

	def __getitem__(self, query ):
		
		if False:
			pass
		
		elif query == 'new':
			
			return Space( self.__files__ )
		
		elif  query == 'backup':
			
			self.__backup__( self )
			
			
		
		elif  query == 'recall':
			
			return self.__recall__()
				
		
		elif  query == 'exec':

			if self['file']:

				space =  Core.execution( self['file'] , self )
				
				# space == self

				space.__called__ = True
				
				return space
			
			else:
				
				raise ValueError("Space with multiple files or empty, monofile space needed. Please provide ext , <space>.<ext>['exec'] " )
		
		
		elif  query == 'marshalize':
			
			Core.marshalize( self )
			
			return self
			
		
		elif  query == 'read':
			
			return self.__read__()
			
			
		elif  query == 'readlines':
			
			return self['read'].split('\n')
		
		
		elif query == 'write':
			
			return self.__write__
			
		elif query == 'rewrite':
			
			return self.__rewrite__	
		

		elif query == 'append':
			
			return self.__append__
			
			
		
			
		elif  query == 'shell': 
			
			return self.__parent__()	
		
		
		elif query == 'exts':
			
			return self.__files_by_ext__()
		
				
		elif query == 'file':
			
			return self.__file__
				
			
		elif query == 'lock_file':
			
			if self.__file__:
				
				return os.path.splitext( self.__file__ )[0] + '.lock'
				
			else:
				
				raise RuntimeError( "\nspace['lock_file'] failed , not space['file']\n" )

		
		elif  query == 'files':
			
			# Changed, before was files by extension, now passed to self.__path__
			
			return self.__files__
			

		elif  query == 'name':
			
			if self.__files__:
				
				return os.path.splitext( os.path.basename(self.__files__[0]) )[0]
			
			else:
				
				return None
				
			
		
		elif   query == 'data':
			
			data = {}
			
			for k,v in self.__dict__.iteritems():
				
				if not self.__islogic__( v ) and not k.startswith( '__' ):
					
					data[k] = v
				
			return data
		
		
		elif  query == 'logic':
			
			logic = {}
			
			for k,v in self.__dict__.iteritems():
				
				if self.__islogic__( v ) and not k.startswith( '__' ):
					
					logic[k] = v

			return logic
		
			
			
		elif  query == 'all_user_data':
			
			data = {}
			
			user_vars = [ x for x in self.__dict__.items() if x not in self.__proto__ ]
			
			for k,v in user_vars:
		
				if not self.__islogic__( v ):
					
					data[k] = v
		
			return data
		
		
		elif  query == 'user_data':
			
			all_data = self['all_user_data']
			
			return dict( [ (k,v) for k,v in all_data.items() if not k.startswith( '__' ) ] )
		

		elif  query == 'all_user_logic':
			
			logic = {}
			
			user_vars = [ x for x in self.__dict__.items() if x not in self.__proto__ ]
			
			for k,v in user_vars:
				
				if self.__islogic__( v ):
					
					logic[k] = v

			return logic

		
		elif  query == 'user_logic':
			
			all_logic = self['all_user_logic']
			
			return dict( [ (k,v) for k,v in all_logic.items() if not k.startswith( '__' ) ] )
			
		
		elif query == 'all':
			
			''' Returns a dict with all logic and data '''
			
			return dict( self['data'].items() + self['logic'].items() )
			
			
		elif query == 'all_user':
			
			''' Returns a dict with all user defined logic and data '''
			
			return dict( self['all_user_data'].items() + self['all_user_logic'].items() )
		
		
	   #elif query == 'info':
	   #	
	   #	return self.__info__()
			
			
		elif query == 'called':
			
			return self.__called__		
			
			
		else:
			
			raise Warning( '''
			
WARNING query not found : [ %s ] %s
Try some of this:
			
          'info' : to print an overview of space"
         'files' : to get a dict with files by extension"
          'name' : to get the common name of all files"
          'data' : to get all data defined in space"
     'user_data' : to get all user data defined in space"
         'logic' : to get all logic defined in space"
    'user_logic' : to get all user logic defined in space\n\n"

			''' % ( query , self.__file__ ) )

			return None
	
	
	
	def __islogic__( self , value ):
		
		if type( value ).__name__ in ['module' , 'type', 'function', 'instancemethod']:
			
			return True
		
		else:
			
			return False
		
		
		
	
		
	def __compile__(self):
		
		import py_compile
		
		for path in self.__files__:
			
			dirname , basename = os.path.split( path )
			name, ext = os.path.splitext( basename )
			
			if ext == '.py':
				py_compile.compile( path )
				print '>> %s file has been Compiled' % basename	
				break
		
	def __marshalize__(self):

		Core.marshalize( self )
				

	
	def __parent__(self):
		
		if self.__files__:
		
			return sop.Shell( os.path.dirname(self.__files__[0]) )
		
		else:
			

			print '\n\nWARNING !!! Accessing parent shell of a fileless space.'
			print '\nIs inusual to get the parent of an empty space, so sop.Void is returned. Check it out!.\n'
			
			return Void( "empty space['parent']" )    
	

	def __rshift__(self, other):
		
		for k,v in vars(self).iteritems():
			if not k.startswith('__'):  
				setattr(other, k, v)
		
		return self
	
	def __lshift__(self, other):
		
		''' space << other 
		
		space << 'path/to/file'
		
		space << object 
		
		'''
		
		typ = type( other ).__name__

		if typ in 'str unicode'.split():
			
			other_space = self['shell']( other )
			
			Core.execution( other_space['file'] , self )
		
		
		else:

			for k,v in vars(other).iteritems():
				if not k.startswith('__'):
					setattr(self, k, v)
		
		return self
	
	
	def __files_by_ext__( self ):
		
		files_by_ext = {}
		
		for f in self.__files__:
			
			dirname, basename = os.path.split(f)
			name, ext = os.path.splitext(basename)
			files_by_ext[ext] = f
		
		return files_by_ext
	
	def __path__(self, ext ):

		files_by_ext = self.__files_by_ext__()
		
		if ext in files_by_ext:
			
			return files_by_ext[ext]

		else:
			
			raise IOError('There is no file with < %s > extension' % ext)
	
	
	def __backup__( self , copy = False ):
		
		if not self['file']:
			
			raise RuntimeError( 'backup needs a monofile space' )


		import shutil
	
		idx = 0
	
		while 1:
		
	
			backup_file = '%s.%04d' % ( self.__file__ , idx )
		
			if not os.path.isfile( backup_file ):
			
				args = self.__file__ , backup_file
			
				if copy:
				
					shutil.copy( *args )
				
				else:	
			
					shutil.move( *args )
			
				break
		
			else:
			
				idx += 1
				
		return backup_file
		
	
	def __validate__( self ):
		
		#print '\nWARNING : USING A EXPERIMENTAL SPACE FEATURE, read, write, append.\n'
		
		if not self.__file__ :
			
			if not os.path.isfile( self.__file__ ):

				raise ValueError("No such file in Space.__file__" )

			else:
				
				raise ValueError("Operation not allowed in space with multiple files, monofile space needed. Please provide ext , < space.<ext> >" )
	
	
	def __rewrite__( self , text , backup = True , accumulate = False ):

		self.__validate__()
		
		current_lines =  self['read']   #[ l for l in self['read'] if l.strip() ]
		
		new_lines = text  #[ l for l in text if l.strip() ]
		
		if current_lines != new_lines:
			
			if backup and current_lines:
			
				self.__backup__( self )
	
			f = open( self.__file__ , 'w' )

			f.write( text )

			f.close()
			
		return self
	
	
	
	def __write__( self , text , backup = True ):
		
		
		self.__validate__()
			
		if backup:
		
			self.__backup__( self )
	
		f = open( self.__file__ , 'w' )
		
		f.write( text )
		
		f.close()
		
		return self
		
		
	
	def __append__( self , new_text, backup = True ):
		
		self.__validate__()
		
		file_text = Normalize.code( self['read'] )	
		
		new_text = Normalize.code( new_text ).split('\n')
		
		old_text = file_text.split('\n') 	
	
		if backup and new_text:

			self.__backup__( self )
		
		
		f = open( self.__file__ , 'a' )

		to_append = '\n' + '\n'.join( new_text ) #( '' if file_text.endswith( '\n' ) else '\n' ) 
		
		f.write( to_append )
		
		f.close()
		
		#print 'APPENDING:\n%s\n' % to_append
		
		return self
		

	def __read__( self ):
		
		self.__validate__()
		
		open( self.__file__ , 'a' ).close()
		
		f = open( self.__file__ )
		code = f.read()
		f.close()
		return code	
	
	
	
	

	#def __update__(self):
	#	
	#	if self.__files__:
	#		
	#		for solver in Solver.Flow:
	#			
	#			solver()(self)
	#	
	#	return self
	
	
	#def __reload__(self , bypass = False):
	#	
	#	if bypass:
	#		
	#		return self
	#	
	#	
	#	if self.__file__:
	#		
	#		return Core.execution( self.__file__ )
	#		
	#	else:
	#		
	#		print '>> WARNING : MultiFile spaces cannot reload' , self.__files__
	#		
	#		return self
	
		
	def __bpath__(self, targets):
		
		
		#print '\nSpace.__bpath__\n'
		
		#print '__bpath__ with targets :' , targets
		
		for target_ext in targets:
			
			#print '*0' , self, self.__files__ , target_ext 
			
			for path in self.__files__:	
				
				#print '*1' , path
				
				dirname, basename = os.path.split(path)
				name, ext = os.path.splitext( basename )

				if ext == target_ext:
					
					#print 'debug: found bpath for targets  ' , self.__files__
					
					#self.__file__ = path
					#self.__folder__  = dirname
					
					return path, dirname, name, ext
					
		return None
	

	def __getattr__(self, att):
		
		exts = {}
		
		if self.__files__:
			
			for f in self.__files__:
				
				exts[ os.path.splitext(f)[-1][1:] ] = f
		
		if att in exts.keys():  # space.py
		
			return Space( [ exts[att] ] )
		
		else:
			
			if self.__called__:
	
				raise AttributeError( """

>> WARNING: Error trying to access '%s' attribute in %s.

This error is produced at least in three occassions:

1. You haven´t call the space relative to:

%s

2. The code you have executed in the space is in error, 
Check terminal output to find the origin of the traceback.

3. If the traceback is raised in line 1 of the document and the line is empty, 
you need to save the document with endline set to LF instead of CRLF ( Windows ).

<< WARNING.

""" % ( att , repr( self ) , self.__files__ )  )
			
			else:
				
				raise AttributeError( """
				
>> WARNING: '%s' attr not found in Space.

Your space hasn´t been called, maybe this is why '%s' attr is not in space. 

Space = %s [ %s ]
Files = %s

<< WARNING.

""" % ( att , att, self['name'] , repr(self) , self['files'] )  )
	
				
	def __str__(self):
		
		
		
		current = vars(self).copy().items()
		
		categories = {}
		userItems  = []
		
		for item in current:
			
			name , value = item
			
			if item in self.__proto__ :
				
				if name.startswith('__'):
					continue
			
				vtype = type(value).__name__
			
				if vtype not in categories.keys():
					categories[vtype] = [name]
				
				else:
					categories[vtype].append(name)
			
			elif item not in self.__proto__ and not name.startswith('__'):
				userItems.append(item)
			
			else:
				pass
		
		
		
		info = '''

Space Listing

    Files:
%s

    System items:
%s		

    User items:	
%s		

/Space Listing
	
		'''
		
		files  = [ '\n        %s' % f for f in  self.__files__ ]
		
		system = [ '\n        %s %s %s' % ( cat , ' '*( 10-len(cat ) ) , atts )  for cat, atts in sorted(categories.items()) ]
		
		user   = [ '\n        %s = %s' % (  name  , repr( value )  )   for name, value in userItems ]
		
		
		
		return info % ( ''.join( files ) , ''.join( system ) , ''.join( user ) ) 
		
		
		


class Shell(object):
	
	
	#def __raw__(self, path ):
	#	
	#	if path:
	#		
	#		path = path.replace('\\', '/')
	#		path = os.path.expandvars( path ) 
	#		
	#		return path
	
	
	#def __rshift__(self, other):		
	#	
	#	all_files   = self.__all_files__
	#	shell_path  = self.__path__
    #
	#	for f in all_files:
	#		name, ext = os.path.splitext( os.path.basename(f) )
	#		space = getattr( self , name )
	#		setattr(other, name, space)
	
	
	#__cwd__ = None
	
	def __new__(cls, path = None , flat = False ):
		

		#if path and not Core.in_domain( path ):
		#	
		#	raise RuntimeError( '\n\n\nShell out of DOMAIN :: %s\n\nAvailables domains are >> %s\n' % ( path, Core.__domains__ ) )
		
		#print '\n\n\nsop.DEBUG : Globals' , globals().keys()
		
		
		self = super(Shell,cls).__new__(cls)
		self.__super__ =  super( Shell, self)
		
		
		if path == None:
			
			if hasattr( main , 'sop_finder' ):
				
				self.__path__ =  Normalize.path( os.path.dirname( main.sop_finder.__file__ ) )
			
			else:
			
				self.__path__ =  Normalize.path( os.path.dirname( sop.__file__ ) )
			
			
		
		#elif path == 0:	
		#	self.__path__ =  Normalize.path( os.getcwd() )
		
		elif path and not os.path.exists(path):
			
			raise IOError( 'path not exists : %s ' % path  )
		
		else:

			self.__path__ = Normalize.path( path )

		
		self.__flat__    =  flat
		
		self.__all_files__   = []
		self.__all_folders__ = []
		
		self.__walk__()
		
		return self
	

	
	def __parent__(self):
		return Shell( os.path.split(self.__path__)[0] )
	
	

	
	def __call__(self, path_element = None,  write = None , recreate = True ): # reset , append are disabled, write only affect on new files      ## append = None reset = False ,
		
		'''
		shell() : Empty Space
		
		shell('') shell('./') : This Path
			
		shell('/some/path') : Absolute Path
		
		shell('some/path') : Relative to shell Path
	
		shell('../') : Parent Path
		
		shell('.../') : Any  number of dots
		
		With no extension always folder  '/this/will/be/folders'
		With extension always file 'file.txt' , any extension
		
		
		'''
		
		if path_element == None:   # Returns an Empty Space
			
			return Space()
			
		
		elif path_element == '' :  # Return same shell
			
			return self
			
		
		else:
			
			path_element = Normalize.path( path_element ) #self.__raw__( path_element )	
			
			points = 0   # this evaluates points at string start
			
			for char in path_element:
				if char == '.':
					points += 1
				else:
					break
		
		
			if not points:
				
				
				if len( path_element ) > 1 and path_element[1] == ':':   # Windows Absolute Path
					
					fullPath = path_element
	
				else:
				
					fullPath = Normalize.join( self.__path__ , path_element )  #  sopbox/folder joined to /other_folder gives you /other_folder		
		
			else:
			
				parent_path = self.__path__
			
				for n in range(points-1):
					
					parent_path = os.path.dirname( parent_path )

				fullPath = Normalize.join( parent_path , path_element[points+1:] ) 
				
		
			# PATH_FIX
	
			fullPath = Normalize.path( fullPath ) 
	
			ext = os.path.splitext( fullPath )[1]
			
			
			if not os.path.exists( fullPath ) and not recreate:
				
				raise RuntimeError, '\nERROR : shell called with ( recreate = False ) , reference path not exists : %s' % path_element
				
			
			elif not ext:

				#print '\n>> DEBUG SOP SHELL ::  NO EXT : fullpath = %s \n\n' % fullPath
				
				if not os.path.exists( fullPath ):
					
					self.__makedirs__( fullPath )
					
					print '\n>> AUTOMATIC folder creation : [...]%s\n' % fullPath[-50:]

					if not os.path.exists( fullPath ):
						
						raise OSError( '\n SOP : No permission to create folder [ %s ]' % fullPath )
					
				
				return Shell( fullPath ) 
				
				#try:
				#except OSError:					
					#pass  # Could not create dir or dir exists
		
			else:
				
				#print '\n>> DEBUG SOP SHELL ::  FILEPATH : fullpath = %s \n\n' % fullPath
				
				folder_path = os.path.dirname( fullPath )
				
				if not os.path.exists( folder_path ):
					
					self.__makedirs__( folder_path )
					
					print '\n>> AUTOMATIC folder creation : " %s "\n' % folder_path
					
					
					
				
				if not os.path.exists( fullPath ):
					

					f = open( fullPath,'a')
		
					print '\n>> AUTOMATIC Space ( file ) creation  [...] %s' % '/'.join( fullPath.split('/')[-6:] ) 
				
					if write:
			
						f.write( write )
			
						print '\n       > file " %s " has been filled with new content.\n' % os.path.basename( fullPath )
		
					f.close()


				return Space( [ fullPath ] )
	
	
	def __makedirs__( self , folder_path ):
				
		if folder_path.startswith( '//' ):

			head = '//'

		elif folder_path.startswith( '/' ):

			head = '/'	

		elif folder_path[1] == ':':

			head = folder_path[:3]

		elif folder_path.startswith( '.' ):

			head = None

		else:

			raise AttributeError( 'Mirar por que empieza este path y corregir en sop.shell >> %s' % folder_path )


		if head:

			tail = head.join(  folder_path.split( head )[1:]  ).split('/')
			
			if head == '//' and len( tail ) > 1: 
			
				folder_in_root = head + '/'.join( tail[:2] ) 
			
			else:
				
				folder_in_root = head + tail[0]
			
			
			
			if tail and not os.path.exists( folder_in_root ):

				raise IOError( '\n\n!!!! Autocreate folders at root level is not allowed directly; path not exists : %s\n\n\n' % ( folder_in_root ) )
		
		

		os.makedirs( folder_path )	
	
	
	
	
	
	def __query__( self, query , items ):
		
		import fnmatch
		
		query_tags = [ i for i in query.split() if i]
	
		if len( query_tags ) == 1:
		
			return items
		
		else:
			
			result = []
			
			for tag in query_tags[1:]:
				
				result.extend(  fnmatch.filter( items , tag )  ) #[ x for x in items if fnmatch.fnmatch( x , tag ) ]
				
			return result
	
	
	def __getitem__(self, query ):
		
		if query == '$DIR':
			
			base_index = len( self['$PATH'] ) + 1
			
			self.__walk__()
			
			exts = []
			
			for solver in Solver.__solvers__:
				
				exts.extend( solver() )

			att_list = []
			
			for f in self.__all_files__:
				
				dirname, basename = os.path.split(f)
				name, ext = os.path.splitext(basename)
				
				if ext in exts:
					
					route = Normalize.join( dirname , name )[base_index:]
					att_list.append(route)
			
			return  sorted( list( set( att_list ) ) )
		
		elif query == '$PARENT':
			
			return self( os.path.dirname( self['$PATH'] ) )
			
		elif query == '$REVEAL':
			
			os.system( "open %s" % self['$PATH'] )	
			
			return self
			
		elif query == '$SPACE':
			
			# forzamos el espacio cuando tenemos un directorio que se llama igual que el espacio 
			#print "%s.*" % self['$NAME']
			
			
			parent = self['$PARENT']
			
			files = parent[ '$FILE_NAMES %s.*' % self['$NAME'] ]
			
			return Space( [ Normalize.join( parent['$PATH'] , f ) for f in files  ] )
		
		
		#elif query == '$FILES':
			
		# USAGE  '$FILES *.py'
		
		
		
		elif query.startswith( '$FILES' ):
			
			self.__walk__()	
			
			return self.__query__( query , self.__all_files__ )		
		
		elif query.startswith( '$FILE_NAMES' ):
			
			content = [ os.path.basename( p )  for p in  self['$FILES']  ]
			
			return self.__query__( query , content )		
		
		
		elif query.startswith( '$FOLDERS' ):

			self.__walk__()

			return self.__query__( query , self.__all_folders__ )
		
		
		elif query.startswith( '$FOLDER_NAMES' ):
			
			content = [ os.path.basename( p )  for p in  self['$FOLDERS']  ]
			
			return self.__query__( query , content )
				
		
		elif query == '$NAME':
			
			return os.path.basename( self.__path__ )
			
		elif query == '$PATH':
			
			return self.__path__
		
		elif query == '$LS':
			
			print '\nListing content for %s shell\n' % self['$NAME']
			
			for item in self['$FOLDERS']:
				
				print '/%s' % os.path.basename( item )
			
			for item in self['$FILES']:
				
				print  os.path.basename( item )
			
			print '\n' , '-'*10
		
		
		elif query == '$WALK':
			
			def avoid( name ):

				return ( name.startswith( '__' ) or name.startswith( '.' ) )
			
			
			def walk_gen():
			
				for P,D,F in os.walk( self['$PATH'] ):
					
					P = Normalize.path( P )
					
					F = [ f for f in F if not avoid(f) ]
					
					D[:] = [ d for d in D if not avoid(d) ]
					
					yield ( P,D,F )
					
			return walk_gen()
		

		
		elif query.startswith( '$GLOB_NAMES' ):
			
			content = self['$FOLDER_NAMES'] + self['$FILE_NAMES']
			
			return self.__query__( query , content )
			
		
		elif query.startswith( '$GLOB_PATHS' ):
			
			content = self['$FOLDERS'] + self['$FILES']
			
			return self.__query__( query , content )
			
			
		
		

			
		
		
		#elif type(query).__name__ in ['str','unicode']:
		#	
		#	self.__walk__()
		#	
		#	if not query:
		#		
		#		return self.__all_files__
		#		
		#	
		#	import re
		#	matched = []
		#	
		#	for f in self.__all_files__:
		#		if re.search( query, f ):
		#			matched.append(f)
		#	
		#	if not matched:
		#		print '\n>> WARNING! query does not match anything : [ %s ]\n' % query
		#	
		#	return sorted( matched )
		
		
		
		
		else:
							
			raise AttributeError( """

>> WARNING query not valid : [ %s ]
	
	? Try <shell>['$DIR'] for a list of file names in compilance with current solvers
	? Try <shell>['$FILES'] for a list of files
	? Try <shell>['$FOLDERS'] for a list of folders
	? Try <shell>[<substring>] for search <substring> in filenames
	
<< WARNING.

""" % query )



		
	def __getattr__(self, att):
		
		if att == '_':		
			return Shell( self.__path__ , flat = True)
		
		elif att == '__':
			return Shell() # root, parent
								
		else:
			return self.__solver__( att )
	
	
	def __bpaths__(self  ):
		
		#print '\nShell.__bpaths__\n'
		
		self.__walk__()
		
		valid_extensions = []

		for solver in Solver.__solvers__:
			
			valid_extensions.extend( solver() )

		
		#print 'debgu valid extensions' , valid_extensions
		
		all_paths = []

		for f in self.__all_files__:
			
			#print  '>>DBG _ALL_FILES__ ::: ', f
			
			path, ext = os.path.splitext( f[len( self.__path__ ) + 1:] )

			if ext in valid_extensions:
				
				all_paths.append(path)


		#all_paths = set(all_paths)  #sorted( list(set(all_paths)) )

		# Get bpaths

		bpaths = []

		for path in all_paths:

			bpath = [self.__path__ ]

			while path:
				path, name = os.path.split(path)
				bpath.insert(1, name )

			
			if bpath not in bpaths:
			
				bpaths.append( bpath )
		
		
		def sort_filter( item ): 
			
			return  str( item )  #str( -1*len(item) ) +
			
		
		bpaths = sorted( bpaths , key = sort_filter  ) #, reverse = True
        
		#print 'DEBUG bpath' + '\n'.join( [ str(x[1:]) for x in bpaths ] )

		return bpaths
		
		
		
	
	def __solver__( self, att ):
		
		matched_files  = []
		matched_folder = None
		
		# NEW!
		
		def filter_name( name ):
			
			private = name.startswith( '__' )
			hidden  = name.startswith( '.' )
			
			if hidden or private: return False	
			else: return True
		
		
		for P,D,F in os.walk( self.__path__ ):
			
			F    = [x for x in F if filter_name(x) ] #x[0] not in ['.']
			D[:] = [x for x in D if filter_name(x) ] #x[0] not in ['.','_']
			
			for f in F:
				name, ext = os.path.splitext(f)
				if att == name:
					
					target_path = Normalize.join( P,f )
					target_path = Normalize.path( target_path )       #os.path.expandvars( target_path ).replace( '\\' , '/' )
					
					matched_files.append( target_path )
			
			for d in D:
				if att == d:
					matched_folder = d
	
		
			if matched_folder:
				
				target_path = Normalize.join(P, matched_folder)
				target_path = Normalize.path( target_path )    #os.path.expandvars( target_path ).replace( '\\' , '/' )
				
				
				context = Shell( target_path )
				
				if matched_files:
					
					for f in matched_files:
						
						ext = os.path.splitext(f)[-1][1:]
						setattr( context, ext , Space( [f] ) )
						
					context.flow = Space( matched_files )
				
				return context
			
			elif matched_files:
				
				return Space( matched_files )
			
			if not self.__flat__:
				break
		
		
		raise AttributeError( 'No file or folder named < %s > in %s' % (att, self.__path__) )#.__parent__()

	
	# NEW! Changed to make 
	# __ private
	# and allow _##_foldername
	
	def __walk__( self ):
		
		self.__all_files__   = []
		self.__all_folders__ = []
		
		for P,D,F in self['$WALK']:
			
			self.__all_files__.extend( [ Normalize.join( P , f ) for f in F ] )
			self.__all_folders__.extend( [ Normalize.join( P , d ) for d in D ] )
			
			if not self.__flat__:
				
				break
		
		return self.__path__ , self.__all_folders__ , self.__all_files__
	
	
	#def __walk__( self, flat = False ):
	#	
	#	#sys.__stdout__.write( '\nDEBUG %s' % self.__flat__ )
	#	
	#	def filter_name( name ):
	#		
	#		return not ( name.startswith( '__' ) or name.startswith( '.' ) )
	#
	#	
	#	self.__all_files__   = []
	#	self.__all_folders__ = []
    #
	#	for P,D,F in os.walk( self.__path__ ):
	#		
	#		#sys.__stdout__.write( '\nDEBUG ...')
	#
	#		F    = [ f for f in F if filter_name(f) ]
	#		D[:] = [ d for d in D if filter_name(d) ]
	#			
	#		
	#		self.__all_files__.extend( [ Normalize.join( P , f ) for f in F ] )
	#		self.__all_folders__.extend( [ Normalize.join( P , d ) for d in D ] )
	#		
	#		if not ( self.__flat__ or flat ):
	#			
	#			break
	#	
	#	return self.__path__ , self.__all_folders__ , self.__all_files__
	

	
	def __str__(self):
		
		
		template = '''

%s Listing

    %s
				
    Folders:
%s
	
    Files:
%s

/%s Listing

	'''  

		flat = 'Flat Shell' if self.__flat__ else 'Shell' 
		
		path = self.__path__
		
		folders = ''.join( [ '\n        [ %s ]' % d for d in self['$FOLDER_NAMES'] ] )
		
		files = ''.join( [ '\n        %s' % f for f in self['$FILE_NAMES'] ] )
		
		return template % ( flat , path ,   folders , files , flat )
		









class Solver(object):
	
	
	
	'''

	# Solver template

	class userSolver( Solver ):

		tag = '< debug tag >'

		targets = [ '.ext' ]

		def __solve__(self):

			self.space
			self.path
			self.dirname
			self.name
			self.ext

	'''
	
	tag = 'default python/marshal'
	
	targets = [ '.py', '.pyc', '.pyo', '.marshal' ]
	
	__solvers__ = []
	
	__debug_print__ = False
	
	
	
	def __init__( self ):
		

		for solver in Solver.__solvers__:
			
			current_targets = solver()
			
			for ext in self.targets:
				
				if ext in current_targets:
					
					current_targets.remove( ext )
					
					#print 'DEBUG : removed target %s from %s solver' % (  ext , solver.tag )
					
			if not current_targets:
				
				#print '>> Solver %s removed from Solver.__solvers__' % ( solver )
				
				Solver.__solvers__.remove( solver )
		
		Solver.__solvers__.append( self )
	

	def __extensions__( self ):
		
		exts = [] 
		
		for solver in Solver.__solvers__:
			
			exts.extend( solver() )
		
		return exts


	def __call__(self , space = None ):
		
		
		# Al solver entra un spacio monofichero, y si se puede se resuelve
		
		
		if not space:
			
			return self.targets
		
		self.space = space
		
		by_extension = space['exts']
		
		for trg_ext in self.targets:
			
			if trg_ext in by_extension.keys():
				
				self.path = by_extension[ trg_ext ]
				
				self.dirname, self.basename , self.name, self.ext  = Normalize.split( self.path )
				
				exec_info = '%s :: [%s]' % ( self.tag , self.basename )

				if sop.Solver.__debug_print__: sys.__stdout__.write( '\n\n    >> %s\n' % exec_info )
						
				self.__solve__()
							
				if sop.Solver.__debug_print__: sys.__stdout__.write('    << %s\n\n' % exec_info )
				
				return self.space
					

		
	def __solve__(self):
		
		if sop.Solver.__debug_print__: sys.__stdout__.write( '\n\nSolving using default python solver\n' )
		
		Core.execution( self.path , self.space )


Solver()


	
	

def __init( main ):
	
	print '\nSpace Oriented Python initialization...'
	
	Expose.object( Shell() , 'sh' ) 
	
	Expose.object( Brain() , 'brain' )
	

	# define cwd ( original )
	
	#if not Shell.__cwd__:		
	#	
	#	Shell.__cwd__ = Shell( os.getcwd() ) #
	#	
	#	#print '?????', os.getcwd()
		
		
		
	
	# Define main.space	
	
	if hasattr( main , '__file__' ):
		
		file_path = Normalize.join( os.getcwd() , main.__file__ )
		
		main.space = Shell()( file_path )
   	
   	elif sys.argv and os.path.isfile( sys.argv[0] ):
    	
		# result in a python interactive session with file args

   		main.space = Shell()( sys.argv[0] )

	else:
		
		# result in a python interactive session without file args
		
		main.space = Space()
	

__init( main )






