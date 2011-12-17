

# this file is evaluated in main



import sys

try:
	
	sys.dont_write_bytecode = True

except:
	
	pass


import sop_finder
import sop

print sh.Help.medula.license['read']

# Nuke Sopbox Structure Configuration

cwd = sop.Expose.object( sh( os.getcwd() ) , 'cwd' )

medula = sop.Expose.object( sh( '..' ) , 'medula' )

local  = sop.Expose.object( medula( 'local' ) , 'local' )


if 'logs' not in medula['$FOLDER_NAMES']:
	
	print 'First Run'
	
	brain.FIRST_RUN = True
	
logs = sop.Expose.object( medula( 'logs' ) , 'logs' )

# expose some handy shells


sop.Expose.modules( 'nuke nukescripts shutil math threading' )
# modules are exposed in main and sop


brain.Lib << medula.system.Lib
# load medula system Lib folder into brain




medula.local( '_init.py' )()
# execute user/local config.init





sop.Core.lap( 'startup.medula.init' )
# start tag lapse 
sop.Core.redirect_output( logs( '%s.init.log' % this.HOSTLABEL )['file']  )
# redirect output to a log file


brain.Lib.include.LOAD_QUEUED_TOOLSETS()
# load all queued toolsets


sop.Core.restore_output( )
# restore output
sop.Core.lap( '/startup.medula.init' )
# stop tag lapse 

#sop.sys.exit()









