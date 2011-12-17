

import random



def mainThread( result , fun , *args , **kwargs ):
	
	if result:
	
		nuke.executeInMainThreadWithResult( fun , args , kwargs )

	else:
		
		nuke.executeInMainThread( fun , args , kwargs )
	



def interactive1():
	
	time.sleep(.0001)
	
	selected_nodes = space.this.SELECTED_NODES
	
	for this in selected_nodes:
	
		x = int( this.NODE.xpos() + random.randint(-0 , 10) )
		y = int( this.NODE.ypos() + random.randint(-10 , 10) )
	
		this.NODE.setXYpos( x , y )

	
	#return True


def init(  ):
	
	
	dots = [ n for n in nuke.allNodes() if n.Class() == 'Dot' ]
	
	
	deselect_all = lambda : [ n.setSelected( False ) for n in nuke.allNodes()]
	
	[ nuke.delete( n ) for n in dotNodes() ]
	
	deselect()
	
	
	
	
	
	




def interactive():
	
	
	
	
	

	
	
	
	deselectAll()
	
	
	
	n = nuke.nodes.Dot().setSelected( True )
	

	nuke.nodeCopy('%clipboard%')
	
	[ nuke.nodePaste('%clipboard%') for i in range(100) ]
	
	[ n.setSelected( True ) for n in dotNodes() ]
	
	nuke.nodeCopy('%clipboard%')
	
	deselectAll()
	
	[ nuke.nodePaste('%clipboard%') for i in range(100) ]
	

	#return True


	

def thread( ):
	
	while True: 
		
		result = Core.execution( space.py['file'] , __TAG__ = True ).interactive()
		
		if not result:
			
			print 'End of game'

			return # mainThread( False , nuke.message , 'End of game' )
		
		

if not hasattr( space, '__TAG__' ):
			
	thread_start = Core.thread( thread ).start

	nuke.executeInMainThreadWithResult( thread_start )
