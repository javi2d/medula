
import sys
try: sys.dont_write_bytecode = True
except: pass



sleep_time = .1

if __name__ == '__main__':
	
	# Evaluated in main

	import sop_finder
	import sop	


	sop.Expose.object( sop.sh( sop.sys.argv[0] )['shell'] , 'ink' )
		
	brain.Lib << ink.Lib
	
	ink( 'Sources/ink_source.py' )
	
	raw_input( """

Ink; I(nteractive)n(u)k(e) is an experimental File Interpreter.

Edit and save 'ink/Sources/ink_source.py' file.
	
Press a key to start interpreting ...""" )
	
	
	while 1:
		
		sop.Core.execution( space['file'] )


else:
		
	# This code is evaluated in a new Space each time
	
	brain( '_sleep_time' , .1 )

	active = False
	
	source = ink( 'Sources/ink_source.py' )

	stats = brain( 'stats' , '' )
	
	new_stats = os.stat( source['file'] )[-2:]
	
	if not stats == new_stats:
		
		active = True
		
		brain.loop_stats_id  = loop_stats_id = brain( 'loop_stats_id' , 0 ) + 1
		
		print '\n'*10
		print '| %s | ink execution loop unit.' % brain.loop_stats_id
		print '_'*50
		print '\n\n'
		
		brain.ink << ink( 'ink.memory' )
		
		#print brain
		
		brain( 'SHARED_CONTEXT' , sop.Space() )
		
		
		
		use_shared_context = brain.ink( 'USE_SHARED_CONTEXT' , True )
		
		#print 'Control' , time.time() , use_shared_context
		#print brain.ink
		
		if not use_shared_context:
			
			brain.SHARED_CONTEXT = sop.Space()
			
			print 'renewed context'
			
		
		
		
		stored_history = False
		
		try:
			
			sop.Core.execution( source['file'] , brain.SHARED_CONTEXT )
			
			#brain.Lib << ink.Lib
			
			if brain.ink( 'STORE_SCRIPT_HISTORY' , True ):
				
				stored_history = brain.Lib.autosave.save( source )
			
			
			
		except:
			
			if brain.ink( 'STORE_IN_ERROR_CODE' , False ):
				
				stored_history = brain.Lib.autosave.save( source )
			
			
			raise
		
		
		finally:
			
			if stored_history:
			
				print '\n\n... script history stored' 
		
		
		
		brain.stats = new_stats
		
		#print '\n\n>>'

	else:
		
		time.sleep( brain._sleep_time )
	
	
	if active:
		
		brain._sleep_time = .01
		active = False
		
	else:
		
		if brain._sleep_time < 5:

			brain._sleep_time += 0.01
		
		#print brain._sleep_time



	
		

