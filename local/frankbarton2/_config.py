
'''
this file is your global medula config file.

- define shells to toolsets

- include or load the toolsets 

- add favourite paths

onInitStage()

onMenuStage()


'''

include = brain.Lib.include




def onInitStage():
	
			
	include.LOAD_TOOLSET(  schema.config   )     # Pure data in memories 
	
	include.THIS( schema.config._this.py )

	include.CALLBACKS( schema.config._cbk.py )
	
	
	schema._home = schema.home
	
	include.TOOLSET( schema._home )  
	
	
	schema._user = schema( 'users/%s_%s' % ( this.HOSTLABEL , this.USER ) )

	include.TOOLSET( schema._user )


	schema._project = schema._user

	include.TOOLSET( schema._project )
	
	
	schema._sessions = schema._user( 'Sessions' )
	
	

		

def onMenuStage():
	
	pass
	
	# add fav paths here
	

	print '\n\n\n-------------------- MenuStage1 ------------------------------\n\n\n'

	include.BOOKMARK( '[ schema ]' , schema['$PATH'] )


	print '\n\n\n-------------------- MenuStage2 ------------------------------\n\n\n'

	include.BOOKMARK( '[ current_unit ]' , this.UNIT_PATH )
	

	print '\n\n\n-------------------- MenuStage3 ------------------------------\n\n\n'

	include.SOURCES_BOOKMARKS()


	print '\n\n\n-------------------- MenuStage4 ------------------------------\n\n\n'

