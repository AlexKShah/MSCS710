import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='root', password='password', database='limon')
cursor = mariadb_connection.cursor()

cursor.execute("CREATE TABLE processes(pid varchar,name varchar, cpu_load FLOAT); INSERT INTO processes VALUES (\"2\",\"python\",1.0), (\"3\".\"chrome\",2.0); SELECT * FROM processes;")
for pid, name, cpu_load in cursor:
    print("pid  name    cpu_load")
    print ("{}  {}       {}").format(pid,name,cpu_load)



