
# this file is evaluated in main ( __main__ namespace )

import sop

sop.Expose.object( sh( os.getcwd() ) , 'cwd' )

sop.Expose.object( sh( '..' ) , 'medula' )

sop.Expose.modules( 'nuke nukescripts shutil math threading' )
## modules are exposed in main and sop


## This is a trigger to show the welcome message to medula
if 'local' not in medula['$FOLDER_NAMES']: brain.FIRST_RUN = True


brain.Lib << medula.system.Lib
## Load medula system Lib folder into brain


## AUTOMATIC LOCAL CONFIGURATION
medula( 'local/_init.py' )()


## AUTOMATIC LOCAL CONFIGURATION
brain( 'Sources' , sop.Brain() )


if not hasattr( sop , 'local' ):
	
	## Local config
	sop.Expose.object(  medula( 'local' )  , 'local' )
	
	# By default local.home is included, this just put the toolset in a queue, this dont load anything yet.
	brain.Lib.include.TOOLSET( local( 'home' ) , recreate = True )
	
	# Pre-Process Sources
	brain.Lib.sources.normalize_host( local.home( 'Brain/Sources.memory' ) )



## INCLUDED TOOLSETS PROCESSING

sop.Core.lap( 'startup.medula.init' )
## Start tag lapse 


#sop.Expose.object( local( 'logs' ) , 'logs' )
#sop.Core.output_redirect( logs( '%s.init.log' % this.HOSTLABEL )['file']  )
## Redirect output to a log file


brain.Lib.include.LOAD_QUEUED_TOOLSETS()
## Load all queued toolsets


#sop.Core.output_restore( )
## Restore output

sop.Core.lap( '/startup.medula.init' )
## Stop tag lapse 


#sop.sys.exit()


