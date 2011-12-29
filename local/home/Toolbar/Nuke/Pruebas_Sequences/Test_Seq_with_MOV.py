

read_nodes_params = []

for P,D,F in os.walk( '/Users/user/Desktop/Medula_Tutorial/FOOTAGE' ):

	D[:] = [ d for d in D if not d.startswith( '.' ) and not d.startswith( '__' ) ]

	seq = medula.knife.Lib.sequence().sequences( P )
	
	print 'DEBUG1 SEQ' , seq
	
	for name , stats in sorted( seq.items() ) :
		
		
		if '.PROXY' in name:
			
			continue

		
		ff, lf, cont = stats
		
		seq_path = Normalize.join( P , name )
		
		fname, ext = os.path.splitext( name )
		
		read_nodes_params.append( [ seq_path , ff, lf ] )

		

#nuke.executeInMainThreadWithResult( LIB_read_creator_thread , ( read_nodes_params ) )

