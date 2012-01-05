

DEFAULT_PATTERN = '$CATEGORY_$UNITID_$LABEL'


	
def process_category( this ):
	
	category = this.VALUES.wm_category
	
	Category =  brain.Categories( category , None , create_att = False ) or Brain()
	
	Category.category = category
	
	Category.params = Category( 'params' , None  ) or 'channels all colorspace linear file_type exr'
	
	if this.VALUES.file_type == ' ' :

		try :

			this.NODE.readKnobs( Category.params )

		except:

			print '\n\nWARNING!!! Fail while reading these knobs params : %s\n\n' % Category.params
	
	
	
	pattern = Category( 'pattern' , None  ) or '$CATEGORY_$UNITID_$LABEL'
	
	TOKENS = {

	'$CATEGORY' : this.VALUES.wm_category.lower() , 
	'$LABEL'    : this.VALUES.wm_label , 
	'$UNITID'   : this.UNIT_ID ,
	'$UNITNAME' : this.UNIT_NAME,

		}
	
	
	for k,v in TOKENS.items():
		
		pattern = pattern.replace( k , str(v) )
	
	
	if '$VERSION' not in pattern:

		pattern += '_$VERSION'
		
		
	Category.pattern = pattern
	

	Category.color = Category( 'color' , None ) or 'Aquamarine'
	
	return Category
	






def build_path( this , return_params = False ):
	
	Category = process_category( this )

	if Category.category == 'disabled':
		
		this.KNOBS.wm_tree.setValue( '----' )
		
		return
	
	prefix = NO_VERSION_FOLDER = Category.pattern.split( '_$VERSION' )[0]
	
	OUTPUT_PATH = Normalize.join( this.UNIT_PATH , brain.Project.OUTPUT , this.VALUES.wm_category  )
	
	done_versions = []
	
	import re
	
	if os.path.exists( OUTPUT_PATH ):
		
		for P,D,F in os.walk( OUTPUT_PATH ):
			
			D[:] = [ d for d in D if d.startswith( NO_VERSION_FOLDER ) ]
			
			for basename in [ f for f in F if f.startswith( NO_VERSION_FOLDER ) ]:
				
				matches = re.findall( "_v\d+" , basename, re.IGNORECASE)
				
				if matches:

					digits = matches[-1][2:]
					
					if digits not in done_versions:
						
						done_versions.append( digits )
	
	render_pattern = Category.pattern.replace( '$VERSION' , 'v%02d' )
	
	next_version = 0	
				
	if done_versions:
		
		next_version = sorted( [ int( x ) for x in done_versions ] )[-1] + 1		
		
	if this.VALUES.wm_overwrite:

		next_version = ( next_version - 1 )
		
	next_version = next_version if next_version > 1 else 1
	
	render_pattern = VERSION_FOLDER = render_pattern % next_version

	ext = ( this.VALUES.file_type.strip() or 'exr' )
	
	ext = { 'targa' : 'tga' , 'jpeg' : 'jpg' }.get( ext , ext )
	
	if ext in 'mov'.split() or this.VALUES.wm_category == 'Snapshot':
		
		render_pattern = render_pattern + '.%s' % ext
	
	else:
	
		render_pattern = render_pattern + '.%04d' + '.%s' % ext
	
	folder = ''
	
	if this.VALUES.wm_folderize:
		
		folder = VERSION_FOLDER if this.VALUES.wm_perversion else NO_VERSION_FOLDER
		
		
	this.KNOBS.wm_tree.setValue( '<b><font size=3 color= "Orange">%s</font></b>' % render_pattern )
	
	OUTPUT_PATH = Normalize.join( OUTPUT_PATH , folder , render_pattern  )

	PROXY_PATH = brain.Lib.sequence.proxy_res_path( OUTPUT_PATH ) if this.VALUES.wm_path_target == 'both' else ''
	
	if this.VALUES.wm_path_target == 'file':

		this.KNOBS.file.fromScript( OUTPUT_PATH ) #fromScript
		this.KNOBS.proxy.fromScript( '' )
		
	elif this.VALUES.wm_path_target == 'both':
		
		this.KNOBS.file.fromScript( OUTPUT_PATH )
		this.KNOBS.proxy.fromScript( PROXY_PATH  )
	

		


	
			
