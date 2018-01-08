
import sys
import os
import StringIO
import psycopg2


DSN = 'dbname=mydebe'

if len(sys.argv) > 1:
  DSN = sys.argv[1]
  print DSN

conn = psycopg2.connect(DSN)
#print "Encoding for this connection is", conn.encoding


curs = conn.cursor()

try:
   curs.execute("CREATE TABLE test_copy (fld1 text, fld2 text, fld3 int4)")
except:
   conn.rollback()
   curs.execute("DROP TABLE test_copy")
   curs.execute("CREATE TABLE test_copy (fld1 text, fld2 text, fld3 int4)")
conn.commit()

# prepare data in a file
io = open('copy_from.txt', 'wr')
data = ['Tom\tJenkins\t37\n',
'Madonna\t\\N\t45\n',
'Federico\tDi Gregorio\t\\N\n',
'Federico\tIori\t\\N\n']
io.writelines(data)
io.close()

# copy data from a file to a table
io = open('copy_from.txt', 'r')
curs.copy_from(io, 'test_copy')
print "1) Copy %d records from file object " % len(data) + \
"using defaults (sep: \\t and null = \\N)"
conn.commit()

io.close()
