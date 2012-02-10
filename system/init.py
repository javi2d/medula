
# this file is evaluated in main ( __main__ namespace )

print '\n\nLoading medula...\n'


# SYSTEM CONFIG


import sop


sop.Core.output_redirect()


## modules are exposed in main and sop
sop.Expose.modules( 'os sys time nuke nukescripts shutil math threading' )

sop.Expose.object( sop.sh( os.getcwd() ) , 'cwd' )

sop.Expose.object( sop.sh( '..' ) , 'medula' )


print '\n\n!!!!! FAIL CHECK NEXT TWO LINES\n\n'

print sop.Normalize.path( '$HOME/.nuke/medula_temp' )

print sop.sh( '$HOME/.nuke/medula_temp' )['$PATH']

sop.Expose.object( sop.sh( '$HOME/.nuke/medula_temp' ) , 'medula_temp' )


# LOCAL CONFIG

sop.tmp.config_code = '''

include = brain.Lib.include

def onInitStage():
	
	brain.Lib.include.TOOLSET( schema )
	
	
def onMenuStage():

	include.BOOKMARK( '[ schema ]' , schema['$PATH'] )
	
'''


sop.tmp.schema_code = '''

SCHEMA = 'home1'

'''


## This is a trigger to show the welcome message to medula
if 'local' not in medula['$FOLDER_NAMES']: brain.FIRST_RUN = True

sop.tmp.schema_brain << medula( 'local/_schema.memory' , write = sop.tmp.schema_code )

sop.tmp.schema_brain( 'SCHEMA' , '' )

sop.tmp.schema_brain( 'LOCAL' , medula.local )


if not sop.tmp.schema_brain.SCHEMA == None:

	## Load medula system Lib folder into brain ( memory , similar to import )
	brain.Lib << medula.system.Lib
	
	if sop.tmp.schema_brain.SCHEMA:
		
		
		sop.Expose.object( sop.tmp.schema_brain.LOCAL( sop.tmp.schema_brain.SCHEMA ) , 'schema' )

		sop.tmp.schema_config = schema( '_config.py' , write = sop.tmp.config_code )

		sop.tmp.schema_config(  onInitStage = lambda : None , onMenuStage = lambda : None  )
		
		print '\n@schema: %s' % sop.tmp.schema_brain.SCHEMA
		
		sop.tmp.schema_config.onInitStage()

		## Start tag lapse 
		sop.Core.lap( 'startup.medula.init' )

		## Load all queued toolsets
		brain.Lib.include.LOAD_QUEUED_TOOLSETS()

		## Stop tag lapse 
		sop.Core.lap( '/startup.medula.init' )
	
	else:
		
		print '\n@schema: < NO SCHEMA >'


print '\n\n\n-------------------- END OF system/init.py file ------------------------------\n\n\n'


sop.Core.output_restore( )


	#sop.sys.exit()






