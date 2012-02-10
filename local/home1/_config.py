

include = brain.Lib.include

def onInitStage():
	
	brain.Lib.include.TOOLSET( schema )
	
	
def onMenuStage():

	include.BOOKMARK( '[ schema ]' , schema['$PATH'] )
	
