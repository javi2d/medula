
# this file is evaluated in main ( __main__ namespace )

import sys
try: sys.dont_write_bytecode = True
except: pass

#import sop_finder
import sop

try: sys.dont_write_bytecode = False
except: pass


#print sh.license['read']


sop.Expose.object( sh( os.getcwd() ) , 'cwd' )

sop.Expose.object( sh( '..' ) , 'medula' )

	
sop.Expose.modules( 'nuke nukescripts shutil math threading' )
## modules are exposed in main and sop


brain.Lib << medula.system.Lib
## Load medula system Lib folder into brain


# Initialize the icons folder
brain.Lib.include.ADD_RECURSIVE( medula.system.Icons )


## This is a trigger to show the welcome message to medula
if 'local' not in medula['$FOLDER_NAMES']: brain.FIRST_RUN = True


## Local config
sop.Expose.object(  medula( 'local' )  , 'local' )


# This line create a default 
local( 'home' )


# Load the Sources.memory file
brain.Sources << local.home( 'Brain/Sources.memory' )

if this.HOSTLABEL not in brain.Sources['names']:
	
	# If current host is not present in Sources.memory the file is dumped with the host added.
	
	brain.Lib.sources.normalize()
	brain.Sources >> local.home.Brain( 'Sources.memory' )

brain.Lib.sources.normalize()


# By default local.home is included, this just put the toolset in a queue, this dont load anything yet.
brain.Lib.include.TOOLSET( local.home , recreate = True )


# Executes the file medula/local/_init.py
local( '_init.py' )()



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


