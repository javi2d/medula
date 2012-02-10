
def normalize( path ):
	
	return sop.Normalize.path( path )


def join( *args ):

	return sop.Normalize.join( *args )



def normalize_padding( path ):
	
	#path = brain.Lib.path.normalize( path )
	
	path = sop.Normalize.path( path )
	
	dirname , basename = os.path.split( path )
	
	pad_count = basename.count('#')
	
	if pad_count:

		basename =  basename.replace( '#' * pad_count , '%' + ( '%02d' % pad_count ) + 'd' )
		
	
	return sop.Normalize.join( dirname , basename )
	

def normalize_name( name ):
	
	normalized = ''

	for char in name:

		normalized += ( char if char.isalnum() else '_' )					

	if normalized and normalized[0].isdigit():

		normalized = '_' + normalized

	return normalized




def brk( path ):
	
	dirname , basename = os.path.split( path )
	name, ext = os.path.splitext( basename )
	
	return dirname , basename , name , ext


def fragment( path  ):
	
	return  [ x for x in normalize( path ).split('/') ]
	


def head( path , start ):
	
	fragmented = fragment( path )
	
	if len( fragmented ) > start:
		
		return '/'.join( fragmented[:start] )
	
	else:
		
		return path
	

def tail( path , start ):
	
	fragmented = fragment( path )
	
	if len( fragmented ) > start:
		
		return '/'.join( fragmented[-start:] )
	
	else:
		
		return path



def version( path ):

	path = sop.Normalize.path( path )

	dirname , basename = os.path.split( path )

	version = 1

	for item in basename.split('_'):

		if item.startswith('v') and item[1:].isdigit():

			version = int( item[1:] )
			break

	return version

	