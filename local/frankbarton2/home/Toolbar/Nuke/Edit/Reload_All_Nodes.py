

print '\n>> Autoreloading nodes:\n'

for node in [ n for n in nuke.allNodes() if 'reload' in n.knobs() ]:
	
	if node['reload'].enabled():
		
		print '    %s reloaded' % node.name()
		
		node['reload'].execute()
		
	if node.Class() == 'Read':
		
		node['find_proxy'].execute()

		seq_color = brain.Lib.sequence.color( node['file'].value() )

		node['tile_color'].setValue( seq_color )

		node.redraw()

		
	if node.Class() == 'Write':
		
		print '    %s refreshed' % node.name()
		
		node['wm_refresh'].execute()
			

print '\n<< Reload done.\n'