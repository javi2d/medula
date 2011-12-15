
print '\n'*10

print 'SOFT_RELOAD_OUTPUT\n\n'

reload( sop )

sh.init() # reload init file
sh.menu() # reload menu file


print '\n\nSUCESSFUL LIBRARY SOFT RELOAD ON' , time.asctime()