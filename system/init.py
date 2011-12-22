
# this file is evaluated in main ( __main__ namespace )

import sys
try: sys.dont_write_bytecode = True
except: pass

#import sop_finder
import sop


#print sh.license['read']

# expose some handy shells

sop.Expose.object( sh( os.getcwd() ) , 'cwd' )

sop.Expose.object( sh( '..' ) , 'medula' )

if 'logs' not in medula['$FOLDER_NAMES']: brain.FIRST_RUN = True
	

sop.Expose.modules( 'nuke nukescripts shutil math threading' )
# modules are exposed in main and sop


brain.Lib << medula.system.Lib
# load medula system Lib folder into brain



# Local config

_medula_tmp_code = '''

local = medula.local

'''

medula_local_config = sop.Brain() << medula( 'local/_config.memory' , write = _medula_tmp_code )

del _medula_tmp_code


sop.Expose.object(  medula_local_config.local  , 'local' )

sop.Expose.object( local( 'logs' ) , 'logs' )



local( '_init.py' )()
# execute _init.py file in "local"


# INCLUDED TOOLSETS PROCESSING


sop.Core.lap( 'startup.medula.init' )
# start tag lapse 

#sop.Core.output_redirect( logs( '%s.init.log' % this.HOSTLABEL )['file']  )
# redirect output to a log file


brain.Lib.include.LOAD_QUEUED_TOOLSETS()
# load all queued toolsets


#sop.Core.output_restore( )
# restore output

sop.Core.lap( '/startup.medula.init' )
# stop tag lapse 

#sop.sys.exit()









