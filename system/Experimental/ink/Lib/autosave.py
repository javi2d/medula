


def _digest( content ):

	import hashlib
	md5 = hashlib.md5()
	md5.update( content )
	return md5.digest()


def save( space ):


	actual_code = space['read']

	last_saved , md5digest = brain( 'autosave' , ( time.time() , _digest( actual_code ) ) )

	#if ( time.time() - last_saved ) > brain( 'autosave_timeout' , 30 ):
	
	if not md5digest == _digest( actual_code ):
	
		#space['backup'] 
		
		save_history( space )
		
		brain.autosave = time.time() , _digest( actual_code )
	
		return True
	
		
	return False
	

def save_history( space ):
	
	history_path = ink( 'History/%s' % '_'.join(  [ str(x) for x in  time.localtime()[:3] ] ) )['$PATH']
	
	import shutil

	idx = 0

	while 1:
	
		backup_file = '%s.%04d' % ( space['file'] , idx )
		
		backup_file = sop.Normalize.join( history_path ,  os.path.basename( backup_file ) )
		
		if not os.path.isfile( backup_file ):
			
			#print backup_file
			
			args = space['file'] , backup_file
			
			shutil.copy( *args )
				
			break
	
		else:
		
			idx += 1
			
	
	
	

