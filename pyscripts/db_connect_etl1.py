#!/usr/bin/env /python


"""db_connect_etl.py:  """


__author__      = "Bachatero aka Sir Lancelot"
__copyright__ =  "What Also Floats In Water? 2014"
__credits__ = ["Stefan Urbanek aka stiivi", "Arthur, King of the Britons"]
__license__ = "All Monty Python FC Fans"


#import  cx_Oracle
import string, cx_Oracle
#import MySQLdb

## Define Oracle connection - format ("username/password@TNSNAME")
ora_conn = cx_Oracle.connect("berger/berger_97")
ora_cursor = ora_conn.cursor()  #Allocate a cursor

ora_cursor.execute("truncate table n2")
ora_cursor.execute("""select n, v from n1""")

#List_Object = []  #create empty list
#for n, v in ora_cursor:
#    try:   #populate it with the cursor results
#        List_Object.append((n, v))
#    except AttributeError:
#        pass

#print str(len(List_Object)) + ' records in the source list object'

#ora_cursor.prepare("""INSERT INTO n2(n,v) VALUES (:n, :v)""")
#ora_cursor.executemany(None, List_Object)
#ora_conn.commit() #COMMIT that shit before it gets away!

ora_cursor.execute("""insert into n2 select * from n1""")
ora_conn.commit() 


ora_cursor.execute("select count(*) from n2")
ora_row_count = ora_cursor.fetchone()
print str(ora_row_count[0]) + ' records inserted into N2 table'

ora_cursor.execute("select count(*) from n2")
pocet = ora_cursor.rowcount
print pocet

ora_conn.close()

exit(0)
