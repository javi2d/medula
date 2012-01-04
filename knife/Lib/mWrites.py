



DEFAULT_PARAMS = 'channels all colorspace linear file_type exr'

DEFAULT_PATTERN = '$CATEGORY_$UNITID_$LABEL'


def build_path( this ):

	category = this.VALUES.wm_category
	
	if category == 'disabled':
		
		this.KNOBS.wm_tree.setValue( '----' )
		return
	
	
	Category = brain.Categories( category , Brain() , create_att = False )
	

	# READ PARAMS FROM CATEGORY BRAIN

	params = ( Category( 'params' , None ) or DEFAULT_PARAMS )

	if this.VALUES.file_type == ' '  :#and not this.KNOB == this.KNOBS.file_type
		
		try :
		
			this.NODE.readKnobs( params )
		
		except:
			
			print '\n\nFail while reading these knobs : %s\n\n' % params
		
	
	# READ PATTERN FROM CATEGORY BRAIN
	
	
	pattern = (  Category( 'pattern' , DEFAULT_PATTERN ) or DEFAULT_PATTERN ) # if pattern == None
	
	
	TOKENS = {

	'$CATEGORY' : category.lower() , 
	'$LABEL'    : this.VALUES.wm_label , 
	'$UNITID'   : this.UNIT_ID ,
	'$UNITNAME' : this.UNIT_NAME,

		}
	
	
	for k,v in TOKENS.items():
		
		pattern = pattern.replace( k , str(v) )
	
	
	if '$VERSION' not in pattern:

		pattern += '_$VERSION'

	
	
		     # No Version Folder Name
	
	prefix = NO_VERSION_FOLDER = pattern.split( '_$VERSION' )[0]
	
	
	
	
	OUTPUT_PATH = Normalize.join( this.UNIT_PATH , brain.Project.OUTPUT , this.VALUES.wm_category  )  #+ '/Output/%s' % 
	
	matches = []
	
	if os.path.exists( OUTPUT_PATH ):
		
		for P,D,F in os.walk( OUTPUT_PATH ):
			
			D[:] = [ d for d in D if d.startswith( NO_VERSION_FOLDER ) ]
			
			matches.extend( [ f for f in F if f.startswith( NO_VERSION_FOLDER ) ] )
		
		#matches = [ f for f in  sh( OUTPUT_PATH )._[ '$FILE_NAMES' ] if f.startswith( prefix ) ]
	
	pattern = pattern.replace( '$VERSION' , 'v%02d' )
	
	version = 0
	
	render_filename =  pattern

	while 1:
		
		version += 1
		
		render_filename = pattern % version
		
		#print render_filename
		
		version_matches = [ f for f in matches if f.startswith( render_filename ) ]
		
		#print version_matches
		
		if not version_matches:
			
			break
	
	
	if this.VALUES.wm_overwrite:
		
		render_filename = pattern % ( ( version - 1 ) or 1 ) 
		
	
	VERSION_FOLDER = render_filename
	
	
	ext = ( this.VALUES.file_type or 'exr' )
	
	ext = { 'targa' : 'tga' , 'jpeg' : 'jpg' }.get( ext , ext )
	
	if ext in 'mov'.split() or category == 'Snapshot':
		
		render_filename = render_filename + '.%s' % ext
	
	else:
	
		render_filename = render_filename + '.%04d' + '.%s' % ext
	

	folder = ''
	
	if this.VALUES.wm_folderize:
		
		if this.VALUES.wm_perversion:
			
			folder = '/%s' % VERSION_FOLDER
			
		else:

			folder = '/%s' % NO_VERSION_FOLDER
	
	filename = '/%s' % render_filename
	
	OUTPUT_PATH += ( folder + filename )

	this.KNOBS.wm_tree.setValue( '<b><font size=3 color= "Orange">%s</font></b>' % render_filename )
	
	PROXY_PATH = brain.Lib.sequence.proxy_res_path( OUTPUT_PATH )

	if this.VALUES.wm_path_target == 'file':

		this.KNOBS.file.fromScript( OUTPUT_PATH ) #fromScript
		this.KNOBS.proxy.fromScript( '' )
		
	elif this.VALUES.wm_path_target == 'both':
		
		this.KNOBS.file.fromScript( OUTPUT_PATH )
		this.KNOBS.proxy.fromScript( PROXY_PATH  )
		
		
	#print '**DEBUG ' , OUTPUT_PATH


