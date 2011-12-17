

if not hasattr( space , 'subspace' ):
	
	while 1:
	
		space['shell']( 'worker_space.py' )( subspace = None )


else:
	
	
	#sh.init()

	time.sleep( 1 )
	
	print '\n\n' , time.asctime()
	
	# interactive
	
	brain.Lib.database = local.main.Lib.database()
	brain.Lib.worker = local.main.Lib.worker()
	
	# /interactive
	
	
	farm = this.FARM
	
	if 'info' in farm['names']:
		
		print farm.info
	
	if 'list' in farm['names']:

		print farm.list
		print farm.list[0]
	
	#print farm.info
		
		

	
	
	
	