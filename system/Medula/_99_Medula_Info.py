
version_memo = Brain() << sh( 'version.memory' )

version = '%s.%s' % ( version_memo( 'major_version' , 0 ) , version_memo( 'minor_version' , 0 ) )

changeLog = version_memo( 'changeLog' , '---' ).split('@')[1]


msg = '''

Medula for Nuke 

Version %s

Copyright (C) 2011  Javier Garcia

This program is free software: you can 
redistribute it and/or modify it under 
the terms of the GNU General Public License.

Read the full medula license at 
<a href="%s">medula/system/Help/Medula_License</a>

ChangeLog: %s

''' % ( version , sh.Medula._99_Medula_License.html['file'] , changeLog )


msg = brain.Lib.html.txt( msg )


nuke.message( msg )