
def changeNodeColor( *args ):
	
	args = tuple( list( args ) + [ 1 ] )
	
	hex_color = '%02x%02x%02x%02x' % args

	tile_color = int( hex_color  , 16 )

	for node in nuke.selectedNodes():

		node['tile_color'].setValue( tile_color )