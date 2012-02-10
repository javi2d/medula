




def Reads():

	def auto_folder_name( file_value ):

		dirname , basename = os.path.split( file_value )

		name = basename.split('.')[0].split('%')[0]

		if name:

			return name

		else:

			return  brain.Lib.path.tail( dirname , 2 ) #os.path.basename( dirname )


	for node in [ n for n in reversed( nuke.selectedNodes() ) if n.Class() in 'Read'.split() ]:

		this = space.this( node )

		file_value = brain.Lib.path.normalize_padding( this.VALUES.file )

		if this.VALUES.proxy:

			proxy_value = brain.Lib.path.normalize_padding( this.VALUES.proxy )

		else:

			proxy_value = brain.Lib.sequence.current_proxy_res_path( this )
			

		yield node , auto_folder_name( file_value ) , file_value , proxy_value , this.VALUES.first , this.VALUES.last
		


def File():
	
	for node in [ n for n in reversed( nuke.selectedNodes() ) if 'file' in n.knobs() ]:

		this = space.this( node )

		file_value = brain.Lib.path.normalize_padding( this.VALUES.file )

		yield node , file_value