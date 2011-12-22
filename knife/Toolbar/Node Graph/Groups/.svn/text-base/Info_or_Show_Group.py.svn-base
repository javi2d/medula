
#!/usr/bin/env python
# encoding: utf-8

"""
Created by Javier Garcia on 2010-07-01.
Copyright (c) 2011 nukeSopbox. All rights reserved.
"""


if nuke.selectedNodes():

	if nuke.selectedNode().Class() == 'Group':

		nuke.showDag( nuke.selectedNode() )
		
		print 0
		
	else:
	
		nuke.display("nukescripts.getallnodeinfo()", nuke.selectedNode()) 
	
		print 1
		
else:
	
	nuke.display("nukescripts.getallnodeinfo()", nuke.Root()) 
	
	