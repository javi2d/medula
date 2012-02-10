
import nuke

def alignHorizontally():

	selected = nuke.selectedNodes()

	if not selected:
	
		nuke.message( 'Select some nodes, please' )

	else:	
	
		byVerticalPosition = sorted( [ ( n.ypos() ,n ) for n in selected ] )
	
		hreference = byVerticalPosition.pop(0)[1].xpos()
	
		for _ , n in byVerticalPosition:
		
			n.setXpos( hreference )
		


if __name__ == '__builtin__':
	
	alignHorizontally()	