



@brain.Lib.decorators.executeThreadWithResult
def fun():

	for i in range( 100 ):
		
		n = nuke.createNode( 'Blur' )
		
		print 'Created Node'
		
		time.sleep(.01)
		
		
		
print fun()