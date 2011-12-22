


for node in [ x for x in nuke.selectedNodes() if x.Class() == 'Read' ]:
	
	this = space.this( node )
	
	if this.VALUES.source_reference:
		
		src_value   = this.VALUES.source_reference
		file_value  = this.VALUES.file

		this.KNOBS.source_reference.fromUserText( file_value )
		this.KNOBS.file.fromUserText( '%s %s-%s' % ( src_value , this.VALUES.first , this.VALUES.last ) )
	
	
	



