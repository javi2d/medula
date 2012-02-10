


def __R3D_Fixer( value ):
	
	ask = True
	
	if not nuke.selectedNodes():
		
		ask = nuke.ask( 'Change all R3D Reads quality to %s ?' % value )
	
		
	if ask:
	

		nodes = [ x for x in ( nuke.selectedNodes() or nuke.allNodes() ) if x.Class() == 'Read' ]

		for n in nodes:

			try:

				n['r3d_decode_resolution'].setValue( value )
				n['r3d_gamma_curve'].setValue( 'Half Floar Linear' )
	
			except NameError:
		
				pass
				print 'Node %s is not a r3d file' % n.name()
