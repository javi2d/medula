

def brain_string():

	brain_strings = []


	for name in brain['names']:
	
		if name not in 'lapses'.split():
		
			item = brain( name )
		
			if type( item ).__name__ == 'Brain':
			
				brain_strings.append(  '%s' % str( item ) )
		
			else:
		
				brain_strings.append(  '%s = %s' % ( name , str( item ) )  )

	return  '\n'.join( brain_strings )


main._temp_brain_string = brain_string

try:
	
	nuke.display( "main._temp_brain_string()"  , None , 'main.brain' )

finally:

	del main._temp_brain_string