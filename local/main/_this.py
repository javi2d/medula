
# Use this file to extend or override the default behaviour of "this" object

# Definitions



# Sources and Project memories are needed in this


# apply default local source 
brain.Sources( this.HOSTLABEL , Brain() )._hostname = this.HOSTNAME	

# apply home sources
brain.Sources << local.home( 'Brain/Sources.memory' )

brain.Lib.sources.normalize()


# apply default project data
brain.Project << medula.local.main.Brain( 'Project.memory' )

# apply user custom project data
brain.Project << local.home( 'Brain/Project.memory' )



def FARM( self ):
	
	return brain.Lib.database.Cursor( local.home( 'Farm/farm.db' )['file'] )
	# Link to farm database


	
def DEFAULT_UNIT_PATH( self ):
	
	
	
	
	return Normalize.join( brain.Project.DEFAULT_RESOURCE , brain.Project.DEFAULT_PROJECT , brain.Project.DEFAULT_UNIT , brain.Project.SCRIPTS )
	



def UNIT_PATH( self ):
	
	''' unit (shot) path is resolved by script name:
	
	1. Script is not saved yet: unit defaults to DEFAULT_UNIT_PATH
	2. Script is saved but not under a /nuke folder : the unit is where script is saved
	3. Script is under /nuke folder: unit is the parent folder of /nuke folder
	
	'''

	if self.SCRIPT_PATH:
		
		base_folder = Normalize.dirname( self.SCRIPT_PATH )
		
		unit_path = base_folder.split( '/' + brain.Project.SCRIPTS )[0]
	
	else:
		
		unit_path = self.DEFAULT_UNIT_PATH
	

		
	# Esta pasa cuando forzamos que la unidad sea equivalente a un projecto, solo deberia ser valido bajo el default resource
	
	dirname , basename = os.path.split( unit_path )

	if basename == brain.Project.SCRIPTS:
	
		return dirname
	
	else:
	
		return unit_path
	
	
	
	

def UNIT_NAME( self ):

	return os.path.basename( self.UNIT_PATH )


def UNIT_SCRIPTS_PATH( self ):	
	

	return Normalize.join( self.UNIT_PATH , brain.Project.SCRIPTS )
	


def UNIT_RESOURCE_PATH( self ):

	unit_path = self.UNIT_PATH

	compatible , match = brain.Lib.sources.compatible_match_cache( unit_path )

	return match



def UNIT_PROJECT_PATH( self ):

	unit_resource = self.UNIT_RESOURCE_PATH

	if unit_resource:
		
		return Normalize.join( unit_resource , self.UNIT_PROJECT_NAME )
		
	else:
		
		return Normalize.join( brain.Project.DEFAULT_RESOURCE , brain.Project.DEFAULT_PROJECT )





def UNIT_PROJECT_NAME( self ):

	unit_resource = self.UNIT_RESOURCE_PATH

	if unit_resource:

		return self.UNIT_PATH.replace( unit_resource + '/' , '' ).split('/')[0]

	else:

		return brain.Project.DEFAULT_PROJECT







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


	




def HTML( self ):
	
	def html( txt , size = 3 , color = 'Silver' , bold = False , center = True ):
		
		txt = txt.replace( '\n' , '<br>')
		
		base_html = '<font size = "%s" color = "%s">%s</font>' % ( size , color , txt )
		
		if bold:
			
			base_html = '<b>%s</b>' %  base_html
			
		if center:
			
			base_html = '<center>%s</center>' %  base_html
		
		return base_html
	
	return html
	
	
def ICON( self ):

	def html( icon , size = 12  ):

		if size:

			html_string = '<center><img src="%s" width="%s"/></center>' % ( icon , size )  #height="%s"
		
		else:
			
			html_string = '<img src="%s"/>' % icon 
		
		return html_string  #, size 

	return html	

