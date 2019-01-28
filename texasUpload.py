import psycopg2

# connection to local postgres dbase

conn = psycopg2.connect("host=localhost dbname=texas user=postgres password=postgres")
cur = conn.cursor()

# read the data from csv file
with open ('CompanyLCMwParent.csv', 'r') as f:

    next(f) #skip header row

    cur.copy_from(f, 'carriers', sep=',', columns=('group_name','carrier_name','rate_eff_date','rate_basis','lcm', 'likely_writing_co', 'rate_relativity'))

conn.commit()

cur.execute('SELECT * FROM carriers')
carriers = cur.fetchall()
conn.close()

# messages to help debugging
if f != "":
    print("put data in texas db")
else:
    print("your data was not loaded")

