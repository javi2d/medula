
#!/usr/bin/env python
# encoding: utf-8

"""

Created by Javier Garcia on 2010-07-01.
Copyright (c) 2011 nukeSopbox. All rights reserved.
"""



if nuke.thisNode().Class() == 'Group':
	
	nuke.tabClose()
	
	nuke.showDag( nuke.thisParent() )