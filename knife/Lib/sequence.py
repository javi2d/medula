



def folder_with_version( sequence_path ):	

	dirname, basename = os.path.split( sequence_path )

	name = basename.split('.')[0].split('%')[0]

	name = ( name or os.path.basename( dirname )  )
	
	return name
	
	
def folder_without_version( sequence_path ):	
	
	
	name = folder_with_version( sequence_path )

	import re 

	matches = re.findall( "_v\d+" , name , re.IGNORECASE)

	if matches:

		return name.split( matches[-1] )[0]
	
	else:
		
		return name
	



def isstill( path ):

	return ( False if '%' in normalize( path ) else True )

def issequence( path ):

	return ( True if '%' in normalize( path ) else False )


def iscomplete( path , firstFrame , lastFrame ):

	pass



#proxy_from_file

def proxy_res_path( path ):
	
	path = brain.Lib.path.normalize_padding( path )
	
	if '.PROXY' in path:
		
		return path
	
	else:
		
		dirname , basename , name , ext = Normalize.split(  path )
		
		proxy_value = Normalize.join(  dirname  , ( name + '.PROXY' + ext ) )

		return proxy_value


def full_res_path( path ):
	
	path = brain.Lib.path.normalize_padding( path )
	
	if '.PROXY' in path:
		
		return ''.join( path.split( '.PROXY' ) )
	
	else:
		
		return path
	


def current_proxy_res_path( this ):

	proxy_value = proxy_res_path( this.VALUES.file )

	if '%' in proxy_value:

		if not os.path.exists( proxy_value % this.VALUES.first ):

			proxy_value = ''

	else:

		if not os.path.exists( proxy_value ):

			proxy_value = ''


	return proxy_value






def frame_path( path , frame ):

	path = brain.Lib.path.normalize_padding( path )

	if '%' in path:

		return path % frame

	else:

		return path







def is_under( ref_path , path , use_cache = True ):
	
	compatible , match = brain.Lib.sources.compatible_match_cache( ref_path ) 
	
	for compatible in compatible:
		
		prefix = ref_path.replace( match , compatible )
		
		if path.upper().startswith( prefix.upper() ): 
			
			return True
	
	return False
	


def is_under_current_unit( path ):

	'''Get the unit path an get all the possible sources, if path starts with any of the possibilities is under unit'''
	
	return is_under( this.UNIT_PATH , path  )
	


def is_under_current_project( path ):

	
	return is_under( this.UNIT_PROJECT_PATH , path  )
	


def is_under_current_source( path ):
	
	if this.SCRIPT_PATH:

		sH , sR = brain.Lib.sources.host_resource( this.SCRIPT_PATH )
		pH , pR = brain.Lib.sources.host_resource( path )
		
		if sH and sH == pH and sR and sR == pR: 
	
			return True


def is_under_current_host( path ):
	
	
	if this.SCRIPT_PATH:
	
		sH , sR = brain.Lib.sources.host_resource( this.SCRIPT_PATH )
		pH , pR = brain.Lib.sources.host_resource( path )
	
		if pH and pH == sH:
		
			return True
	

def is_bound( path ):
	
	pH , pR = brain.Lib.sources.host_resource( path )
	
	if pH and pR:
		
		return True
	
	

	
	
def color( path ):
	
	colors = { 'green' : 1744785407 ,  'violet' : -881131521 , 'blue' : 1114505215 ,  'darkGrey' : 2054847231 , 'grey' : -960051457 , 'pale_green' : 2864482559 }
	
	
	if path.startswith( brain.Project.DEFAULT_RESOURCE ):

		node_color = colors['pale_green']
	
	
	elif this.SCRIPT_PATH:	
		
		#print 'Color path : ' , brain.Lib.sources.host_resource( this.SCRIPT_PATH ) , is_under_current_unit( this.VALUES.file )
	
		if is_under_current_unit( path ): 
		
			node_color = colors['green'] 

		elif is_under_current_host( path ):
		
			node_color = colors['violet']
	
		elif is_bound( path ):
		
			node_color = colors['blue']
					
		else:
				
			node_color = colors['darkGrey']

	else:
		
		node_color = colors['grey']
	

	return node_color	






def autoproxy( this ): # seems like not used

	''' Fills proxy knob based on file knob if at least first proxy file  frame exists'''

	if this.CLASS == 'Read':

		proxy_value = proxy_from_file( this.VALUES.file )

		first_proxy_frame = frame_path( proxy_value , this.VALUES.first ) #first frame path

		if os.path.isfile( first_proxy_frame ):

			this.KNOBS.proxy.fromUserText( proxy_value )

		else:

			this.KNOBS.proxy.fromUserText( '' )



	else: # inclusive Write node 

		node_knobs = this.KNOBS['names']

		if 'file' in node_knobs and 'proxy' in node_knobs:

			proxy_value = proxy_from_file( this.VALUES.file )

			this.KNOBS.proxy.fromUserText( proxy_value )



def active_node_path( node ):

	# TODO return file or proxy values based on root.proxy state or return file if file is present or return None if node has not any file knob

	pass

















def LIB_disociated( folder_path ):

	disociated = {}
	
	for f in sh( folder_path )['$FILE_NAMES']:
		
		alfa_string = ''
		
		for char in f:
			
			if char.isdigit() and not alfa_string:
				
				alfa_string += '#'
			
			
			elif char.isdigit() and not alfa_string[-1] == '#':
				
				alfa_string += '#'
			
			elif not char.isdigit():
				
				alfa_string += char
					
					
		digits_string = ''
		
		for char in f:
			
			digits_string += ( char if char.isdigit() else ' ' )
			
		digits = [ i for i in digits_string.split() if i ]
		
		
		if alfa_string in disociated:
			
			disociated[ alfa_string ].append( digits )
			
		else:
			
			disociated[ alfa_string ] = [ digits ]

	return disociated.items()	



def LIB_best_solution_index(  all_digits ):
	
	sets = {}
		
	for digits in all_digits:
	
		for i in range( len( digits ) ):
		
			if i in sets:
			
				if digits[i] not in sets[i]:
		
					sets[i].append( digits[i] )
			
			else:
			
				sets[i] = [ digits[i] ]
	
	
	best_index = None
	
	solution_len = 0
	
	
	if sets:
		
		for index , frames in sets.items():
			
			frames_len = len( frames )
			
			if  frames_len > solution_len:
				
				best_index = index
				
				solution_len = frames_len
		
		if frames_len == 1:
			
			best_index = None
		
		
	return best_index
	
	
	
	
	
		
		
def sequences( folder_path ):

	if not os.path.exists( folder_path ):
		
		return [ ]

	sequences = {}
	
	for name , all_digits in LIB_disociated( folder_path ):

		index = LIB_best_solution_index( all_digits )
		
		if index == None: # Single Element without numeric reference
			
			if '#' in name:
				
				for dig in all_digits[0]:
					
					name = name.replace( '#' , dig , 1 )
			
			
			sequences[ name ] = [ 1 ]
			
			continue
		
		else:
			
			#print name , all_digits
						
			for digits in all_digits:
				
				seq_name = name
				
				for i in range( len( digits ) ):
					
					if i == index:
						
						seq_name = seq_name.replace( '#' , '@' , 1 )
					
					else:
						
						seq_name = seq_name.replace( '#' , digits[i] , 1 )
					
				if seq_name not in sequences:
					
					sequences[ seq_name ] = [ digits[ index ] ]
					
				else:
					
					sequences[ seq_name ].append( digits[ index ] )
	

	for name , frames in sequences.items():
			
		if '@' in name:
			
			padding = str( len( frames[-1] ) ).zfill( 2 )
			
			values = sequences[ name ]
			
			del sequences[ name ]
			
			name = name.replace( '@' , '%' + padding + 'd' )
			
			first_frame = int( values[0] )
			
			last_frame  = int( values[-1] )
			
			sequential = ( len( values ) == ( last_frame - first_frame + 1 ) )

			sequences[ name ] = [ first_frame , last_frame , sequential ]
			
		elif len( frames ) == 1:

			sequences[ name ] = [ None , None , True ]
	
		
			
	return sequences	
		
		#print '\n', name , '%s-%s' % ( frames[0] , frames[-1] ) 
		















