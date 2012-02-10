


memory_space = local( 'Brain/Exclusions.memory' )

brain.Exclusions << memory_space


exclusions = brain.Exclusions( 'excluded' , [] )

for node , file_value in brain.Lib.selection.File():
	
	_ , ext = os.path.splitext( file_value )
	
	if ext not in exclusions:
		
		exclusions.append( ext )

		
brain.Exclusions >> memory_space



#tmp = sop.Brain() << memory_space
#
#tmp << brain.Exclusions
#
#tmp >> memory_space
#