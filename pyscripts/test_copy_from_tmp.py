
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

source_file = "/Volumes/HOME/Downloads/test_copy_from1.txt"

# copy data from a file to a table
#io = open('copy_from.txt', 'r')
io = open(source_file, 'r')
#curs.copy_from(io, 'test_copy_from')
curs.copy_from(io, 'test_copy_from',sep='|')
#print "1) Copy %d records from file object " % len(data) + \
#"using defaults (sep: \\t and null = \\N)"
#"using defaults (sep: \| )"
conn.commit()

io.close()
