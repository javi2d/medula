

def scripts( shell_or_path ):
	
	" Under shell or under SCRIPTS folder , paths relative to shell "
	
	
	shell = Normalize.shell( shell_or_path )
	
	SCRIPTS = brain.Project.SCRIPTS
	
	if SCRIPTS in shell['$FOLDER_NAMES']:
		
		scripts =  [ '%s/%s' % ( SCRIPTS , x ) for x in shell( SCRIPTS )['$FILE_NAMES *.nk'] ]
	
	else:
		
		scripts = shell['$FILE_NAMES *.nk']

	return scripts
	


def is_unit( shell_or_path ):
	
	shell = Normalize.shell( shell_or_path )
	
	if brain.Project.SCRIPTS in shell['$FOLDER_NAMES']:
		
		return True
		
	else:
		
		return False


def is_project( shell_or_path ):

	shell = Normalize.shell( shell_or_path )
	
	path = shell('..')['$PATH']
	
	if path in brain.Lib.sources.compatible( path ):
		
		return True
		
	else:
		
		return False
	
	
def project_name( path ):
	
	match = brain.Lib.sources.match_cache( path )
	
	if match:
		
		return path.replace( match + '/' , '' ).split('/')[0]
		



def load_toolset( this , avoid = [] ):
	

	pass
	

	
	
	

def host_resource_list():
	
	hr_list = []
	
	for H , R , path in brain.Lib.sources.alive_resources():
		
		hr_list.append( '%s/%s' % ( H, R ) ) 
		
	return hr_list





def projects( host = this.HOSTNAME , avoid = []):
	

	# return projects
	
	projects = []
	
	for H , R , path in brain.Lib.sources.alive_resources():
			
		if H not in avoid:
			
			res_sh = sh( path )
			
			for project in res_sh['$FOLDER_NAMES']:
	
				print '\n\n' , H,R,project
				
				for P,D,F in res_sh( project )['$WALK']:
					
					P = Normalize.path( P )
					
					D[:] = [ d for d in D if '.' not in d ]
				
					print '.',
					
					if is_unit( sh(P) ):
						
						print '\n' , P
						
						D[:] = []
									
	print '\nEOF Project Scan'
		#print '\n@project.projects 1' , H , this.HOSTNAME
		
		



def units( project_shell ):
	
	EXCLUDE_HOSTS = 'NAS3D Sledgenas'.split()
	
	for H , R , path in brain.Lib.sources.alive_resources():
		
		if H not in EXCLUDE_HOSTS:		
			
			print '\nProcessing %s/%s : ' % ( H , R ) 		
			
			RES_SH = sh( path )
		
			for project in RES_SH['$FOLDER_NAMES']:
				
				print '     ' , project
				
				PRJ_SH = RES_SH( project )			
					
				for P,D,F in Normalize.walk( PRJ_SH['$PATH'] ):
 									
					if brain.Project.SCRIPTS in [ d.lower() for d in D ]:
						
						D[:] = []
					
						RELATIVE_UNIT = P.replace( PRJ_SH['$PATH'] + '/'  ,  '' )
						
						yield PRJ_SH , RELATIVE_UNIT , H , R
	
	
	
	# Return relative to project_shell paths to units 

