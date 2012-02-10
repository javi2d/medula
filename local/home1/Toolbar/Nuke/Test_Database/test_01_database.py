

brain.Lib.database = medula.knife.Lib.database()

con = brain.Lib.database.Connection( 'test.db' )


'''

All tables into database are homogeneous

table_name

name    |  value
----------------
'var'   | '100'
		|
'table' |  NULL  ???? Table reference


'''

# print tables in database connection

print dir( con )



# this is a table object

table = con( 'table_name' )  

# print list of names in table

print dir( table )


# 

print table.items()



# get the 'value' column associated to 'item name'

table[ 'item name' ] 


# set the 'value' column associated to 'item name' 

table[ 'item name' ] = [ 1 , 'DONE' , 'hi' ]

# delete row associated to 'item name' 

del table[ 'item name' ] 

# cross reference to other table 

table[ 'table' ][ 'value_name' ]




tasks = con( 'tasks' )

tasks 




