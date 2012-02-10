

import uuid
import shelve
#import inspect
#
#print dir( inspect.currentframe() )

import random





class shelf:
	
	def __init__( self , *args ):
		
		self.args = args
	
	def __enter__( self  ):

		self.db = shelve.open( *self.args )
		
		self.db['__busy__'] = True
		
		return self.db
		
	def __exit__( self, type, value, traceback ):
		
		self.db['__busy__'] = False
		
		self.db.close()


#def thread1( thread_id = uuid.uuid4() ):

space << sop
		
threads = [ ]

for i in range( 200 ):
	
	thread_id = 'Space%s' % i
	
	spc = space['shell'].receiver
	
	thread = Core.thread( spc , src_space = space  )
	
	threads.append( thread )

[ t.start() for t in  threads ]











	
	
#space['shell'].receiver()
	







## lock
#
#with shelve.open( 'test01.shelve' ) as d:
#	
#	
#

# flush

#with shelve.open( 'test01' ) as d:
#
#	#print d
#
#	d['hostname'] = this.HOSTNAME
#		
#	#d['test'] = space
		

## unlock
#
#with shelve.open( 'test01.shelve' ) as d:
#
#	d['__busy__'] = False
#