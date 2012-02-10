



for i in range( 10 ):
	
	
	
	
	with src_space.shelf( 'test01' ) as d:
		
		#print thread_id
		
		print '>>>' , d['data'] , 
		
		sleep = src_space.random.random()
		
		d['data'] = sleep , src_space.thread_id
		
		print d['data']
		
		
		
	#time.sleep( random.random() )






#import pickle
#
#space = pickle.load( open( 'test01.pickle' ) )
#
#print dir( space )
#

#
#import shelve
#
#import marshal
#
#d = shelve.open( 'test01' ) 
#
#print d
#
##print  marshal.loads( d['test'] ) 
##
#exec marshal.loads( d['test'] )
#