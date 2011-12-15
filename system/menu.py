#!/usr/bin/env python
# encoding: utf-8

"""
nukeSopbox > menu.py

Created by Javier Garcia on 2010-07-01.
Copyright (c) 2011 nukeSopbox. All rights reserved.
"""


sop.Core.lap( 'startup.medula.menu' )

sop.Core.redirect_output( logs( '%s.init.log' % this.HOSTLABEL )['file']  )
# redirect output to a log file


brain.Lib.include.SHELL2MENU( sh.Medula , 'Nuke' )
brain.Lib.include.SHELL2MENU( sh.Help , 'Nuke' )

local( '_menu.py' )()
# execute user/local config.menu


brain.Lib.include.GUI_LOAD_QUEUED_TOOLSETS()
# Process GUI stuff for queued toolset




sop.Core.restore_output( )

sop.Core.lap( '/startup.medula.menu' )

sop.Core.lap( '.startup' )

if brain( 'FIRST_RUN' , False , create_att = False ):
	
	def delayed_msg():
	
		sop.time.sleep(.75)

		nuke.executeInMainThread( nuke.message , ( 'nuke medula sucessfully installed' , ) )

	sop.Core.thread( delayed_msg ).start()



	
#sop.sys.exit()