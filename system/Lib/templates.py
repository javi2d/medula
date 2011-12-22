

# Hay que implementar inputs and outputs and current connections



# No utilizado por nada



def save_selection_as_template( target_shell_alias ):

	tshell = getattr( main , target_shell_alias , None )
	
	if not tshell:
		
		raise AttributeError( '\nError: %s is not defined as shell so you cannot save template into that shell' % target_shell_alias )
		
	

	if this.SELECTED_NODES:
	
		default_path = Normalize.join( tshell( 'Template' )['$PATH']  , os.path.basename( this.UNIT_PROJECT_PATH )    )

		template_file = nuke.getFilename( 'Save Selection As Template ...' , '*.nk' , default = Normalize.join( default_path , 'untitled_template' )   , type = 'save' )

		if template_file:

			if not template_file.endswith( '.nk' ):
			
				template_file += '.nk'
		
			sh( default_path )
		
			nuke.nodeCopy( template_file )

			sh.init()
			sh.menu()
		
		else:
		
			print '\n>> Save as template operation cancelled by user.\n'
		
	else:
		
		nuke.message( 'Save as template operation cancelled,\nyou need to select some nodes.' )