


print '\n-> medula/mdl/__init__.py'

"""

module: mdl
	
	platform: windows,mac,linux
	synopsis: Suite base , pure python
	moduleauthor: Javier Garcia <javi2d@invalid.com>

"""

import sys
sys.dont_write_bytecode = True

'logging'
import logging
logging.basicConfig( format='%(levelname)s: %(filename)+12s -> %(message)s', level = logging.DEBUG  )
log = logging.getLogger(__name__)

'modules'
import uber
import shell
import data
import net
import sources


