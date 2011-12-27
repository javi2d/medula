
#!/usr/bin/env python
# encoding: utf-8

"""
Created by Javier Garcia on 2011-12-08.
Copyright (c) 2011 nukeSopbox. All rights reserved.
"""


if nuke.selectedNodes():

	nuke.display("nukescripts.getallnodeinfo()", nuke.selectedNode()) 
		
else:
	
	nuke.display("nukescripts.getallnodeinfo()", nuke.Root()) 
	
	