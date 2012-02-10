
print '\n'*10

print 'SOFT_RELOAD_OUTPUT\n\n'

reload( sop )

sop.sh.init() # reload init file
sop.sh.menu() # reload menu file


print '\nSUCESSFUL LIBRARY SOFT RELOAD AT' , time.asctime()