
# Use this file to extend or override the default behaviour of "this" object

# Definitions

# Sources and Project memories are needed in this


def FARM( self ):
	
	return brain.Lib.database.Cursor( local.home( 'Farm/farm.db' )['file'] )
	# Link to farm database


	
#def DEFAULT_UNIT_PATH( self ):
#	
#	return sop.Normalize.join( brain.Project.DEFAULT_RESOURCE , brain.Project.DEFAULT_PROJECT , brain.Project.DEFAULT_UNIT , brain.Project.SCRIPTS )
	



def UNIT_PATH( self ):
	
	''' unit (shot) path is resolved by script name:
	
	1. Script is not saved yet: unit defaults to brain.Project.DEFAULT_RESOURCE
	2. Script is saved but not under a /nuke folder : the unit is where script is saved
	3. Script is under /nuke folder: unit is the parent folder of /nuke folder
	
	'''

	if self.SCRIPT_PATH:
		
		base_folder = sop.Normalize.dirname( self.SCRIPT_PATH )
		
		unit_path = base_folder.split( '/' + brain.Project.SCRIPTS )[0]
	
	else:
		
		unit_path = brain.Project.DEFAULT_RESOURCE 
	

		
	# Esta pasa cuando forzamos que la unidad sea equivalente a un projecto, solo deberia ser valido bajo el default resource
	
	dirname , basename = os.path.split( unit_path )

	if basename == brain.Project.SCRIPTS:
	
		return dirname
	
	else:
	
		return unit_path
	
	
	
	

def UNIT_NAME( self ):

	return os.path.basename( self.UNIT_PATH )


def UNIT_SCRIPTS_PATH( self ):	
	

	return sop.Normalize.join( self.UNIT_PATH , brain.Project.SCRIPTS )
	


def UNIT_RESOURCE_PATH( self ):

	unit_path = self.UNIT_PATH

	compatible , match = brain.Lib.sources.compatible_match_cache( unit_path )

	return match



def UNIT_PROJECT_PATH( self ):

	unit_resource = self.UNIT_RESOURCE_PATH

	if unit_resource:
		
		return sop.Normalize.join( unit_resource , self.UNIT_PROJECT_NAME )
		
	else:
		
		return brain.Project.DEFAULT_RESOURCE    #sop.Normalize.join( brain.Project.DEFAULT_RESOURCE , brain.Project.DEFAULT_PROJECT )





def UNIT_PROJECT_NAME( self ):

	unit_resource = self.UNIT_RESOURCE_PATH

	if unit_resource:

		return self.UNIT_PATH.replace( unit_resource + '/' , '' ).split('/')[0]

	else:

		return os.path.basename( brain.Project.DEFAULT_RESOURCE )   #brain.Project.DEFAULT_PROJECT







def UNIT_ID( self ):

	unit_id = []

	found = False

	for item in self.UNIT_NAME.split( '_' ):


		if item.isdigit() or item[:-1].isdigit():  # to allow 001 or 001B 

			unit_id.append( item )
			found = True

		elif found  and not item.isdigit():

			break

		else:

			unit_id.append( item )


	return '_'.join( unit_id )


	






