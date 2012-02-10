

def tokenize( source ):
	
	import cStringIO
	import tokenize , token

	source = cStringIO.StringIO( source )

	bffr = [[]]
	
	TOKENS = []
	
	for toktype, toktext, (srow,scol), (erow,ecol), line in tokenize.generate_tokens( source.readline ):
		
		tokenID = token.tok_name[toktype]
		
		if toktype == 4: # a statement ends
			
			bffr.append( [] )
		
		else: # in statement
			
			item_in_statement = ( tokenID , toktext )
			
			if tokenID in 'NL NEWLINE'.split() and not bffr[-1]:
			
				continue
							
			else:
				
				bffr[-1].append( item_in_statement )
				
	# filter items
	
	level = 0
	
	for token_list in bffr:
		
		token_list = [ x for x in token_list if x[0] not in 'COMMENT NL NEWLINE'.split() ]
		
		while 1:
		
			tkn , txt = token_list[0]
		
			if tkn == 'INDENT':
					
				level += 1
				token_list.pop(0)
				
			elif tkn == 'DEDENT':
					
				level -= 1
				token_list.pop(0)
				
			else:
				
				break
				
		yield level , token_list 		
		


def tokenize_classes( source ):
	

	if not source.endswith('\n'):
		
		source += '\n'
	
	prev_level = 0
	
	result = []

	for level , token_list in tokenize( source ):
		
		if level == 0 and token_list[0][1] == 'class':
			
			active = True
		
		elif level == 0 and not token_list[0][1] == 'class':
			
			active = False
			
		if active:
		
			if level > prev_level:
			
				result.append( '[' )
	
			elif level < prev_level:
		
				for i in range(	prev_level - level ):
		
					result.append( ']' )
					
			result.append( token_list )		
		
			prev_level = level
		
	result = result + [']']*( result.count('[') - result.count(']') )

	return result
		
