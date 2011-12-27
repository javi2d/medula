
def html( txt , size = 3 , color = 'Silver' , bold = False , center = True ):
	
	txt = txt.replace( '\n' , '<br>')
	
	base_html = '<font size = "%s" color = "%s">%s</font>' % ( size , color , txt )
	
	if bold:
		
		base_html = '<b>%s</b>' %  base_html
		
	if center:
		
		base_html = '<center>%s</center>' %  base_html
	
	return base_html
	
	

def icon( icon , size = 12  ):

	if size:

		html_string = '<center><img src="%s" width="%s"/></center>' % ( icon , size )  #height="%s"
	
	else:
		
		html_string = '<img src="%s"/>' % icon 
	
	return html_string  #, size 
