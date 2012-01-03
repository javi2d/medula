
'''
This file is about manipulation of data contained in Brain/Sources.memory

Sources.memory define structures like this

class <HOSTLABEL>:
	
	_hostname = <HOSTNAME>
	
	<RESOURCE> = [ < aka path to local resource > , ...  ] , [ < aka path to remote resource > ... ]

Where <HOSTLABEL> is equal to normalized <HOSTNAME>

<RESOURCE> refer to a folder where projects are housed, <RESOURCE> is a label

First list contains the local paths from where the <RESOURCE> is reached 

Second list contains the remote paths from where the <RESOURCE> is reached 


class My_Host:
	
	_hostname = 'My Host'
	
	PROJECTS1 = [ '/Volumes/disk1/Projects' ] , [ '//My Host/disk1/Projects' , '/Volumes/My Host/disk1/Projects' ]


'''


def walk( ):
	
	hosts = brain.Sources['names']
	
	for host in hosts:
		
		hostname = brain.Sources( host )( '_hostname' , host ) 
			
		if this.HOSTNAME.lower() == hostname.lower():
			
			# put current hostname first 
			
			hosts.remove( host )
			hosts.insert( 0 , host )
	
	
	for host in hosts:
		
		for resource in [ r for r in brain.Sources( host )['names'] if not r.startswith('_') ] :
			
			hostname = brain.Sources( host )( '_hostname' , host ) 
			
			local_resources , remote_resources = brain.Sources( host )( resource )

			#local_resources = [ brain.Lib.path.normalize( path ) for path in local_resources ]
			#remote_resources = [ brain.Lib.path.normalize( path ) for path in remote_resources ]

			yield ( host , hostname , resource , local_resources , remote_resources )


def add_current_host_to_sources():
	
	if this.HOSTLABEL not in brain.Sources['names']:
		
		# Add current host to Sources
		
		brain.Sources( this.HOSTLABEL , Brain() )._hostname = this.HOSTNAME
		
		brain.Sources >> local.home.Brain( 'Sources.memory' )
		
		
		

def normalize():
	
	#print '\n\n>> Normalizing Sources'

	for H , HN , R , LR , RR in walk():


		LR[:] = [ Normalize.path( p ) for p in LR ]
		RR[:] = [ Normalize.path( p ) for p in RR ]
		
		#print brain.Sources( H )( R )
	
	#print 'debug end Normalize Sources'
	


def host_resource( path ):

	for H , HN , R , LR , RR  in  walk():
		
		#print 'DEBG HOST_RESOURCE' , HN , this.HOSTNAME , path , R , LR , RR
		
		to_review = ( LR + RR if HN.lower() == this.HOSTNAME.lower() else RR )
		
		for resource in to_review:

			if path.startswith( resource ):

				return H , R
				
	return None , None

def host( path ):
	
	H, R = space.host_resource( path )
	
	return H
	


def resource( path ):

	H, R = space.host_resource( path )
	
	return R





# DEPRECATED

def valid_resource( host , resource ):

	LR , RR = brain.Sources( host )( resource )
	
	for path in reversed( RR + LR ):
		
		if os.path.isdir( path ) and os.listdir( path ):
	
			return path



def alive_path( host , resource ):
	
	LR , RR = brain.Sources( host )( resource )
	
	paths = RR[:]
	
	if host.lower() == this.HOSTNAME.lower():
		
		paths += LR		
	
	timeout = 30
	
	for path in paths:
		
		alive_resources = brain( 'alive_resources' , {} )
		
		if path in alive_resources and ( time.time() - alive_resources[ path ] ) < timeout:
			
			return path 
		
		
		# Cambiado a que devuelva el recurso incluso vacio
		
		elif os.path.isdir( path ): # and os.listdir( path ):
			
			brain( 'alive_resources' , {} )[ path ] = time.time()
			
			return path
	
	


def alive_resources():
	
	alive = [ ]
	
	for H , HN , R , LR , RR in walk():
		
		path = alive_path( H , R )
		
		if path:
			
			alive.append( ( H, R , path ) )
	
	return alive




def compatible( path , host = None ):
	
	if host == None:
		
		host = this.HOSTNAME
	
	
	# compatible means a list of paths that are compatible with the passed path
	
	# host is used to retrieve compatible paths from other hosts and relink filenames 
	
	
	for H , HN , R , LR , RR  in  walk():
		
		if HN.lower() == host.lower():
			
			for resource in LR + RR:
				
				if path.startswith( resource ):
					
					return LR + RR
		
		else:
		
			for remote_resource in RR:

				if path.startswith( remote_resource ):

					return RR
			
	return []

		
def match( path , host = None ):
	
	return compatible_match( path , host = None )[1]		
	

def match_cache( path , host = None ):

	return compatible_match_cache( path , host = None )[1]
	
	
def compatible_match( path , host = None ):
	
	if host == None:
		
		host = this.HOSTNAME
	
	# this will return a list of compatible paths with arg 'path' and the match itself
	
	compatible = space.compatible( path , host )
	
	for pth in compatible:
		
		#print '[ sources.py ] ' , pth 
		
		if path.startswith( pth ):
			
			return compatible , pth
	
	return [] , None



def compatible_match_cache( path , host = None ):
	
	if host == None:
		
		host = this.HOSTNAME
	
	
	# this will return a list of compatible paths with arg 'path' and the match itself
	
	cache = brain.Sources( '__cache' , {} )
	
	key = ( path , host )
	
	if key not in cache:
		
		cache[ key ] = compatible_match(  path , host )
	
	return cache[ key ]





def __relink( this , knob ,  source_host = None ):
	
	# find file and proxy knobs in Node
	
	# get the file value and check folder

	print '\n\nDEBUG __RELINK 01 (WORKING)' , this.NODE.name() , this.NODE.hasError()
	
	knob_path = this.VALUES( knob )

	dirname , basename = os.path.split( knob_path )
	
	if not os.path.isdir( dirname ):
		
		compatible_paths = []
		
		print '\nDEBUG TESTING     ' , dirname.lower()
	
		for H , HN , R , LR , RR  in  walk():
		
			to_review = ( LR + RR if HN.lower() == this.HOSTNAME.lower() else RR )
		
			for resource in to_review:
			
				print '      COMPARING WITH' , resource.lower()

				if dirname.lower().startswith( resource.lower() ):

					compatible_paths.append( resource )
	
		print 'DEBUG FOUND COMPATIBLE PATHS' , this.NODE.name() , compatible_paths
				

	
	#compatible, match = compatible_match_cache( knob_value , host )


	#if not os.path.isdir( dirname ):
	#
	#	host = ( source_host or this.HOSTNAME )
	#
	#	compatible, match = compatible_match_cache( knob_value , host )
	#	
	#	if not host == this.HOSTNAME:
	#	
	#		local_compatible , local_match = compatible_match_cache( knob_value , this.HOSTNAME )
	#		
	#		if local_match:
	#			
	#			compatible = local_compatible + [ c for c in compatible if c not in local_compatible ]
    #
	#
	#	for comp in [ c for c in compatible if not c == match ]:
	#	
	#		test_dirname = dirname.replace( match , comp )
	#	
	#		print 'Testing : '  
	#	
	#		if os.path.isdir( comp ):
	#		
	#			print 'Relinking %s : %s >> %s' % ( this.NODE.name() , match , comp )
	#			
	#			new_knob_value = Normalize.join( test_dirname , basename)
	#			
	#			this.KNOBS( knob ).setValue( new_knob_value )
	#			
	#			brain( '_relink_changes' , [] ).append( ( this.KNOBS( knob ) , new_knob_value , knob_value ) )
	#			
	#			return
	#	
	#	msg = 'Cannot be relinked %s : %s %s' % ( this.NODE.name() , host , match )
	#	
	#	sys.__stdout__.write( '\n%s\n' % msg )				

		
# USED ONLY in Root_Facility tab , the procedure is moved to the callback 

def relink_read_nodes( knob = 'file' , source_host = None ):
	
	brain.relink_changes = []
	
	for n in nuke.allNodes():

		if knob in n.knobs() and not n.Class().startswith('Write'):
			
			__relink( this(n) , knob , source_host )
						


# NOT USED 

def relink_write_nodes( knob = 'file' , source_host = None ):
	
	brain.relink_changes = []
	
	for n in nuke.allNodes():

		if knob in n.knobs() and n.Class().startswith('Write'):

			__relink( this(n) , knob , source_host )

# NOT USED 

def relink_all_nodes( knob = 'file' , source_host = None ):
	
	brain.relink_changes = []
	
	for n in nuke.allNodes():

		if knob in n.knobs():

			__relink( this(n) , knob , source_host )






