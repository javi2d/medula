

local_config =  None # '../myCompanyName' or absolute paths  /Volumes/Disk/myCompanyName

main_toolset = 'main'


'''
local_config 

	redefine this variable to change the local folder

main_toolset
	
	redefine this variable to change the main toolset

'''


if local_config:
	
	local = sop.Expose.object( medula( local_config ) , 'local' ) 


local( "%s/_init.py" % main_toolset )()







