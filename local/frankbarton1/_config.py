
'''
this file is your global medula config file.

- define shells to toolsets

- include or load the toolsets 

- add favourite paths

onInitStage()

onMenuStage()


'''


local = sop.Expose.object( space['shell'] , 'local' )

include = brain.Lib.include

def onInitStage():
	

	# global config
	
	include.LOAD_TOOLSET(  local.Config )     # Pure data in memories 
	
	# global extensions
	
	include.THIS( local.Config._this.py )

	include.CALLBACKS( local.Config._cbk.py )
	
	
	# toolsets config
	
	local._home = local
	
	include.TOOLSET( local._home )  
	
	
	local._user = local( 'Profiles/users/%s_%s' % ( this.HOSTLABEL , this.USER ) )

	include.TOOLSET( local._user )


	local._project = local._user

	include.TOOLSET( local._project )
	
	
	local._sessions = local._user( 'Sessions' )
	
	

		

def onMenuStage():
	
	pass
	
	# add fav paths here
	
	include.BOOKMARK( '[ local ]' , space.local['$PATH'] )

	include.BOOKMARK( '[ current_unit ]' , this.UNIT_PATH )
    
	include.SOURCES_BOOKMARKS()




