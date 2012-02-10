

def inject_src_host():
	
	if 'source_host' in nuke.Root().knobs():
		
		if this.ROOT.VALUES.source_host != this.HOSTNAME:
		
			this.ROOT.KNOBS.source_host.setValue( this.HOSTNAME )
		
			print '\nUpdated Root.source_host = %s' % this.HOSTNAME



#def version_and_pattern( path ):
#	
# 	'''Given a filename with version
#	
#	filename_id_v00.ext
#	
#	returns  int current_version, str pattern
#	
#	'''
#	import re 
#	
#	dirname , basename , name , ext = sop.Normalize.split( path )
#	matches = re.findall( "_v\d+" , name, re.IGNORECASE)
#
#	version = None
#	pattern = path
#	
#	if matches:
#	
#		digits = matches[-1][2:] # Last match from char 2  _v 0X
#		
#		version_padding = '_v%' + str( len ( digits ) ).zfill( 2 ) + 'd' # %0Xd
#		
#		name = name.replace( matches[-1] , version_padding )
#		
#		pattern = sop.Normalize.join( dirname , name + ext )
#		
#		version = int(digits)
#	
#	return version , pattern
	


#def next_version( path ):
#
#	version, pattern = version_and_pattern( path )
#	
#	dirname , basename , name , ext = sop.Normalize.split( pattern )
#	
#	if version == None:
#	
#		pattern = sop.Normalize.join( dirname , name + '_v%02d' + ext )
#		version = 1
#	
#	
#	name_id = name.split('%')[0]
#	versions = sop.sh( dirname )[ '$FILE_NAMES %s*' % name_id ]
#	
#	if not versions:
#		
#		return pattern % ( version + 1 )
#		
#	else:
#		
#		last_version, _ = version_and_pattern( versions[-1] )
#	
#		return pattern % ( last_version + 1 )



def last_version( dirname , reference ): # reference can be 
	
	import re
	
	matches = re.findall( "_v\d+" , reference , re.IGNORECASE)
	
	last_version = 0
	
	if matches:
		
		reference = reference.split( matches[-1] )[0]
	
	for P,D,F in sop.Normalize.walk( dirname ):
		
		matches  = [ re.findall( "_v\d+" , f , re.IGNORECASE) for f in F if f.startswith( reference ) ]

		versions = [ int( m[-1][2:] ) for m in matches if m ] 

		if versions:
			
			last_version = versions[-1]
			
		break
				
	return last_version	
	
	


def next_session():
	
	sessions_scripts_path = sop.Normalize.join( brain.Project.DEFAULT_RESOURCE , 'nuke' )
	
	session_script_prefix = 'Session'
	
	session_script_path = sop.Normalize.join( sessions_scripts_path , session_script_prefix + '_v01' ) 
	
	if os.path.exists( sessions_scripts_path ):
		
		last_script_version = last_version( sessions_scripts_path , session_script_prefix )
		
		session_script_path = sop.Normalize.join( sessions_scripts_path , session_script_prefix + '_v%02d' % ( last_script_version + 1 ) )
	
	return session_script_path
	
	
	

def saveScript():

	script_path = this.SCRIPT_PATH
	
	#print 'DEBUG script.saveScript' , repr( script_path )
	
	if script_path:

		inject_src_host()
		
		nuke.scriptSave()		

	else:

		saveScriptAs()

	
	

def saveScriptAs():
	

	inject_src_host()
	
	default_path = ( this.ROOT.VALUES.name or next_session() )  #

	script_path = nuke.getFilename( 'Save Script As...' , '*.nk' , default = default_path , type = 'save' )
	
	if script_path:
		
		dirname, basename , name, ext = sop.Normalize.split( script_path )
		
		if os.path.exists( script_path ):
			
			last_script_version = last_version( dirname , name )
			
			if not last_script_version:
				
				next_script_version = name + '_v01'
			
			else:
				
				import re

				matches = re.findall( "_v\d+" , name , re.IGNORECASE)
				
				next_script_version = name.replace( matches[-1] , '_v%02d' ) % ( last_script_version + 1 ) 
				
		
			choice = nuke.choice( 'saveScriptAs' , 'File already exists' , [ 'raise to %s.nk' % next_script_version , 'overwrite %s' % basename  ] )
			
			if choice == 0:
				
				name = next_script_version
						
						
		if '/' + brain.Project.SCRIPTS not in dirname:
		
			dirname = sop.Normalize.join( dirname , brain.Project.SCRIPTS )
	
		sop.sh( dirname )
	
		nuke.scriptSaveAs( sop.Normalize.join( dirname , name + '.nk' ) , overwrite = 1 )

	


def saveSelection( default_path = None , include_root = False ):

	if this.SELECTED_NODES:
	
		default_path = ( default_path or this.UNIT_SCRIPTS_PATH + '/' )
		
		if not default_path.endswith('/'):
			
			default_path += '/'
		
		template_path = nuke.getFilename( 'Save Selection...' , '*.nk' , default = default_path   , type = 'save' )
		
		if not template_path:
			
			raise RuntimeError('\n>> Save Selection... Dialog Cancelled.\n')
		
		
		if template_path.endswith('/'):
			
			msg = 'ERROR! Invalid Script Name.'
			
			if nuke.GUI:
				
				nuke.message( msg )
				
			raise RuntimeError( msg )
		
		
		
		if template_path:
			
			template_path = template_path.strip()
			
			if not template_path.endswith( '.nk' ):

				template_path += '.nk'
			
			
			tfolder , tbasename = os.path.split( template_path )
			tname , text = os.path.splitext( tbasename )
			
			sop.sh( tfolder )

			pattern_list = tname.split( '_' )
			
			last_item = pattern_list[-1]
			
			if last_item.startswith( 'v' ) and last_item[1:].isdigit():
				
				pattern_list[-1] = 'v%0' + str( len( last_item[1:] ) ) + 'd'
				
			else:
				
				pattern_list.append( 'v%02d' )
				
			pattern = '_'.join( pattern_list )
			
			version = 0
			
			while 1:

				version += 1

				test_path = sop.Normalize.join( tfolder , pattern % version ) + text

				if not os.path.exists(  test_path  ):
					
					tmp_script = sop.sh( brain.Project.DEFAULT_RESOURCE )( '__tmp/clipboard.nk' )['file']

					nuke.nodeCopy( tmp_script )
					
					universal_script = '\n'.join( sop.sh( tmp_script )['readlines'][2:] )
					
					if include_root:
						
						root_toScript = nuke.Root().writeKnobs(  nuke.WRITE_ALL | nuke.WRITE_NON_DEFAULT_ONLY  | nuke.TO_VALUE | nuke.TO_SCRIPT |  nuke.WRITE_USER_KNOB_DEFS )
						
						universal_script = 'Root {\n%s\n}\n' % root_toScript  + universal_script

					sop.sh( test_path )['rewrite']( universal_script )
					
					break
			
			#sop.sh.init()		
			#sop.sh.menu()
			
			print '\n>> Saved template as:\n\n  ..%s\n' % brain.Lib.path.tail( test_path , 3 )
			
		else:

			print '\n>> Save as template operation cancelled by user.\n'

	else:

		print '\n>> Save as template operation cancelled , you need to select some nodes.\n'


		


def copyScript( folder , script_name = None , folderize = True ):	
	
	script_name = ( script_name or os.path.basename( this.ROOT.VALUES.name ) )
	
	basename , ext = os.path.splitext( script_name )

	unit_scripts_shell = sop.sh( this.UNIT_SCRIPTS_PATH  ) #space.unit_path()
	
	if folderize:
		
		target_folder =  unit_scripts_shell( '%s/%s' % (folder , basename) )['$PATH']
	
	else:
		
		target_folder =  unit_scripts_shell( folder )['$PATH']  # relativo siempre a unit/nuke folder
	
	import glob
	
	matches = glob.glob( '%s/*%s' % ( target_folder , script_name ) )
	
	index = 0
	
	if matches:
		
		last_item = sorted( matches )[-1]
			
		basename = os.path.basename( last_item )
		
		prefix = basename.split('_')[0]
		
		if prefix.isdigit():
			
			index = int( prefix )
			
	target_path = '%s/%04d_%s' % ( target_folder , index + 1 , script_name )
	
	if os.path.exists( this.ROOT.VALUES.name ) :
	
		import shutil
	
		shutil.copy( this.ROOT.VALUES.name , target_path  )
    
		main.brain.last_autosaved_script = target_path
		
		print '\n>> Script Backup:\n'
		
		print '          source script : ' , this.ROOT.VALUES.name.split('/nuke/')[-1]
		print '          target script : ../nuke/%s' % target_path.split('/nuke/')[-1]
		
		
		return target_path
		
	else:
		
		main.brain.last_autosaved_script = ''
		
		return ''
		


	


	
	
			
		

	
