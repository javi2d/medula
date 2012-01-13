

def setFlags( knob, flags):
	
	flags = flags.split()
	
	for flag in flags:
		
		nkflag = getattr( nuke, flag , None )
		
		if nkflag!= None:
		
			knob.setFlag( nkflag )


def clearFlags( knob , flags ):
	
	flags = flags.split()
	
	for flag in flags:
		
		nkflag = getattr( nuke, flag , None )
		
		if nkflag!= None:
		
			knob.clearFlag( nkflag )
	
	
def tabKnob( Label = 'tab Knob' , Value = 0 , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #

	knob = nuke.Tab_Knob( 'tabKnob' , Label, Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob	
	
Tab_Knob = tabKnob

def txtKnob( Label = 'txtKnob' , Value = '' , Tooltip = ' strKnob has not tooltip ', flags = '' , clearflags = '' ):
	
	knob = nuke.Text_Knob( 'txtKnob' , Label, Value )	
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob


Text_Knob = txtKnob



def xyKnob( Label = 'xyKnob' , Value = [ 0.0 , 0.0 ] , Tooltip = ' xyKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.XY_Knob( 'xyKnob' , Label )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

XY_Knob = xyKnob




def xyzKnob( Label = 'xyzKnob' , Value = [ 0.0 , 0.0 , 0.0 ] , Tooltip = ' xyzKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.XYZ_Knob( 'xyzKnob' , Label )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

XYZ_Knob = xyzKnob


def whKnob( Label = 'whKnob' , Value = [ 0.0 , 0.0 , 0.0 ] , Tooltip = ' whKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.WH_Knob( 'whKnob' , Label )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

WH_Knob = whKnob




def bboxKnob( Label = 'bboxKnob' , Value = [0,0,0,0] , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #

	knob = nuke.BBox_Knob( 'bboxKnob' , Label )

	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

BBox_Knob = bboxKnob


def uvKnob( Label = 'uvKnob' , Value = [ 0.0 , 0.0 ] , Tooltip = ' uvKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.UV_Knob( 'uvKnob' , Label )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

UV_Knob = uvKnob



def colorKnob( Label = 'colorKnob' , Value = [0,0,0] , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #
	
	knob = nuke.Color_Knob( 'colorKnob' , Label )
	
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Color_Knob = colorKnob


def acolorKnob( Label = 'acolorKnob' , Value = [0,0,0,0] , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #

	knob = nuke.AColor_Knob( 'acolorKnob' , Label )

	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

AColor_Knob = acolorKnob

def boolKnob( Label = 'boolKnob' , Value = False , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #

	knob = nuke.Boolean_Knob( 'boolKnob' , Label ) #, Label	
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Boolean_Knob = boolKnob


def scriptKnob( Label = 'scriptKnob' , Command = '' , Tooltip = ' no tooltip ' , flags = '' , clearflags = '' ):

	knob = nuke.Script_Knob( 'scriptKnob' , Label )
	knob.setCommand( Command )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Script_Knob= scriptKnob



def bttnKnob( Label = 'bttnKnob' , Command = '' , Tooltip = ' no tooltip ' , flags = '' , clearflags = '' ):

	knob = nuke.PyScript_Knob( 'bttnKnob' , Label )
	knob.setCommand( Command )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

PyScript_Knob = bttnKnob

def enumKnob( Label = 'enumerationKnob' , Value = [] , Tooltip = 'enumerationKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.Enumeration_Knob( 'enumerationKnob' , Label, Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Enumeration_Knob = enumKnob

def menuKnob( Label = 'menuKnob' , Value = {'Empty/empty':''} , Tooltip = 'menuKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.Pulldown_Knob( 'menuKnob' , Label, Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob


def strKnob( Label = 'strKnob' , Value = '' , Tooltip = ' no tooltip ', flags = '' , clearflags = '' ): #
	
	knob = nuke.EvalString_Knob( 'strKnob' , Label, Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

EvalString_Knob = strKnob


def fileKnob( Label = 'fileKnob' , Value = '/' , Tooltip = ' no tooltip ' , flags = '' , clearflags = '' ):

	knob = nuke.File_Knob( 'fileKnob' , Label )
	knob.setValue( Value )
	#knob.fromUserText( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

File_Knob = fileKnob


# supported by nodes
######################
# array subclasses knobs


def floatKnob( Label = 'floatKnob' , Value = 0.0 , Tooltip = ' floatKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.Double_Knob( 'floatKnob' , Label )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Double_Knob = floatKnob


def intKnob( Label = 'intKnob' , Value = 0 , Tooltip = ' intKnob has not tooltip ', flags = '' , clearflags = '' ):

	knob = nuke.Int_Knob( 'intKnob' , Label, 0 )
	
	#knob = nuke.Array_Knob( 'intKnob' , Label, 0 )
	knob.setValue( Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Int_Knob = intKnob


def txtboxKnob( Label = 'txtKnob' , Value = '' , Tooltip = ' strKnob has not tooltip ', flags = '' , clearflags = '' ):
	
	knob = nuke.Multiline_Eval_String_Knob( 'txtboxKnob', Label, Value )
	knob.setTooltip( Tooltip )
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	return knob

Multiline_Eval_String_Knob = txtboxKnob



def linkKnob( Label = None , Value = 'label' , Tooltip = ' no tooltip ' , flags = '' , clearflags = '' ):
	
	knob = nuke.Link_Knob( 'linkKnob' , Label )
	knob.setLink( Value )
	
	if Label == '':
		
		knob.setLabel( '' )
	
	else:
		
		knob.setLabel( ( Label or knob.getLink() ) )
		
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )
	
	return knob	

Link_Knob = linkKnob


# Specials
##############
# 



	

def idKnob( prefix = 'uuid' ):
	
	import uuid

	knob = nuke.Text_Knob( 'id' , 'id_knob' , '_'.join( [prefix , str(uuid.uuid4()) ] )  )
	knob.setVisible(False)
	return knob

def sepKnob( msg = '' , flags = '' , clearflags = ''):
	
	knob = nuke.Text_Knob( 'sep' , '' , msg )	
	setFlags( knob,  flags )
	clearFlags( knob,  clearflags )	
	return knob


def nullKnob():

	knob = nuke.Text_Knob( 'sep' , '' , ' ' )
	return knob


def errorKnob( name , error = None ):
	
	error = error or 'ERROR!'
	
	knob = nuke.Text_Knob( name , '%s' % name ,  '<font size=3 color="red"> %s </font>' % error )#<p></p>
	return knob
	
		
def beginGroup( Label = '' ):
	
	knob = nuke.Tab_Knob( Label , Label , nuke.TABBEGINGROUP)
	
	return knob

#BeginTabGroup_Knob = beginGroup

def endGroup( idx ):
	
	knob = nuke.Tab_Knob('endGroup%s' % idx , '', nuke.TABENDGROUP)
		
	knob.setFlag( nuke.STARTLINE )
	
	return knob

#EndTabGroup_Knob = endGroup




