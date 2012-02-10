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

## Redirect output to __stdout__
sop.Core.output_redirect()


if not sop.tmp.schema_brain.SCHEMA == None:
	
	# Initialize the icons folder
	brain.Lib.include.ADD_RECURSIVE( sop.sh.Icons )


	brain.Lib.include.SHELL2MENU( sop.sh.Medula , 'Nuke' )
	

	if sop.tmp.schema_brain.SCHEMA:

		print '\n\n\n-------------------- BREAKPOINT Before Process GUI ------------------------------\n\n\n'

		sop.tmp.schema_config.onMenuStage()

		print '\n\n\n-------------------- 1 ------------------------------\n\n\n'

		brain.Lib.include.GUI_LOAD_QUEUED_TOOLSETS()
		## Process GUI stuff for queued toolset


		print '\n\n\n-------------------- 2 ------------------------------\n\n\n'

		#load queued bookmarks
		brain.Lib.include.BOOKMARKS()

		print '\n\n\n-------------------- BREAKPOINT After Process GUI ------------------------------\n\n\n'


print '--------- %s %s ----------\n\n\n' % ( sop.Core.date() , sop.Core.time() )



print '\n\n\n-------------------- END OF system/init.py file ------------------------------\n\n\n'






sop.Core.output_restore( )


sop.Core.lap( '/startup.medula.menu' )

print 



sop.Core.lap( '.startup' )


if brain( 'FIRST_RUN' , False  ):
	
	def delayed_msg():
	
		sop.time.sleep(.75)

		nuke.executeInMainThread( nuke.message , ( 'nuke medula successfully installed.\n\nA new toolset called "home" has been\ncreated under medula/local folder' ) )

	sop.Core.thread( delayed_msg ).start()

del brain.FIRST_RUN
	
	

#sop.sys.exit()



