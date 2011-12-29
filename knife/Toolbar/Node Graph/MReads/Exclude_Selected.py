






exclusions = brain.Exclusions( 'excluded' , [] )

for node , file_value in brain.Lib.selection.File():
	
	_ , ext = os.path.splitext( file_value )
	
	if ext not in exclusions:
		
		exclusions.append( ext )
		

memory_space = local.home( 'Brain/Exclusions.memory' )

tmp = Brain() << memory_space

tmp << brain.Exclusions

tmp >> memory_space
