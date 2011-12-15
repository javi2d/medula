

def tokenize( source ):
	
	import cStringIO
	import tokenize , token

	source = cStringIO.StringIO( source )

	bffr = []
	
	TOKENS = []
	
	for toktype, toktext, (srow,scol), (erow,ecol), line in tokenize.generate_tokens( source.readline ):
	
		tokenID = token.tok_name[toktype]

		bffr.append( ( tokenID , toktext ) )
		
		
		if tokenID in 'NEWLINE NL':
			
			if len( bffr ) > 1:
			
				item = (  bffr , line )
			
				TOKENS.append( item )

			bffr = []
		
		
		
	return TOKENS


def __line_level( line ):
	
	line_level = 0

	for c in line:
		
		if c == '\t': line_level += 1	
		else: break
	
	return line_level

	
	
def tokenize_classes( source ):
	
	if not source.endswith('\n'):
		
		source += '\n'
	
	level = 0
	
	result = []
	
	for tokens , line in tokenize( source ):

		tokenID , tokenText = tokens[0]

		if tokenID == 'NL':
			
			#print '*  ' , tokens
			
			continue
		
		elif tokenID == 'INDENT':
			
			# subidas de uno en uno

			result.append( '[' )
			level += 1
			
		elif tokenID == 'DEDENT':
					
			for i in range(	 level - __line_level( line )  ):
			
				result.append( ']' )
				level -= 1
		
			
		tokens = [ (ID,TK) for ID,TK in tokens if ID not in 'INDENT DEDENT'.split()  ]
		
		result.append( tokens )

	return result
		
