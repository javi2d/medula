



group = nuke.selectedNode()

if group and group.Class() == 'Group' :
	
	default = local._user['$PATH'] + '/Toolbar/Nodes/Gizmos/Gizmo.gizmo'
	
	gizmo_path = nuke.getFilename( 'Export As Gizmo...' , '*.gizmo' , default = default , type = 'save' )
	
	if gizmo_path:
		
		if not gizmo_path.endswith( '.gizmo' ):
			
			gizmo_path += '.gizmo'
		
		tmp_script = sh( brain.Project.DEFAULT_RESOURCE )( '__tmp/clipboard.nk' )['file']
		
		nuke.nodeCopy( tmp_script )
		
		group_code = '\n'.join( sh( tmp_script )['readlines'][2:] ).replace( 'Group' , 'Gizmo' , 1)
			
		sh( gizmo_path )['rewrite']( group_code , backup = False )
		
		print '\nGizmo saved to %s' % gizmo_path
		
		#brain.User
	
	else:
		
		raise RuntimeError( 'Cancelled Save As Gizmo dialog')



