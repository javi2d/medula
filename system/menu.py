#!/usr/bin/env python
# encoding: utf-8

"""
nukeSopbox > menu.py

Created by Javier Garcia on 2010-07-01.
Copyright (c) 2011 nukeSopbox. All rights reserved.
"""






sop.Core.lap( 'startup.medula.menu' )

#sop.Core.output_redirect( logs( '%s.init.log' % this.HOSTLABEL )['file']  )
## Redirect output to a log file


# Initialize the icons folder
brain.Lib.include.ADD_RECURSIVE( sh.Icons )


brain.Lib.include.SHELL2MENU( sh.Medula , 'Nuke' )


medula.local( '_menu.py' )()
## Execute user/local config.menu


brain.Lib.include.GUI_LOAD_QUEUED_TOOLSETS()
## Process GUI stuff for queued toolset

brain.Lib.include.ADD_FAV( '[ local ]' , local['$PATH'] )

#sop.Core.output_restore( )


sop.Core.lap( '/startup.medula.menu' )

print 

sop.Core.lap( '.startup' )

if brain( 'FIRST_RUN' , False  ):
	
	del brain.FIRST_RUN
	
	def delayed_msg():
	
		sop.time.sleep(.75)

		nuke.executeInMainThread( nuke.message , ( 'nuke medula successfully installed.\n\nA new toolset called "home" has been\ncreated under medula/local folder' ) )

	sop.Core.thread( delayed_msg ).start()

#sop.sys.exit()