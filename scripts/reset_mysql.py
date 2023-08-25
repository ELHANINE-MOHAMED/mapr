import mysql.connector

# Set up connection to MySQL server
mydb = mysql.connector.connect(
    host = "localhost",
    port = 3306,
    user="root",
    password="mapr",
    database="CDR"
)

# Create cursor object
mycursor = mydb.cursor()

# Define list of tables to drop
tables_to_drop = [
    "alcatel_tbl",
    "epgw_tbl",
    "ericsson_tbl",
    "esgw_tbl",
    "fixe_tssi",
    "huawei_tbl",
    "ims_tbl",
    "mmp_tbl",
    "nokia_tbl",
    "ocsrec_tbl",
    "ocssms_tbl",
    "ocsvou_tbl",
    "pgw_tbl",
    "rsgsn_tbl",
    "sgw_tbl",
    "siemens_tbl",
    "tssa_tbl"
]

# Loop through list of tables and drop each one
for table in tables_to_drop:
    sql = "DROP TABLE IF EXISTS `{}`".format(table)
    mycursor.execute(sql)

# Commit changes to database
mydb.commit()

# Close cursor and database connection
mycursor.close()
mydb.close()
