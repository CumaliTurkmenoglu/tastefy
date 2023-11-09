import mysql.connector
# Replace these with your database credentials
db_host = '151.106.97.51'#'srv449.hstgr.io'  # Hostinger MySQL server address
db_port = 3306  # MySQL default port
db_username = 'u189214306_info'
db_password = 'Serhildancml.123'
db_database = 'u189214306_usda2'

# Connect to the MySQL database
connection = mysql.connector.connect(
    user=db_username,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_database,
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Now, you can execute SQL queries using the 'cursor' object
cursor.execute("SELECT * FROM foods")

# Fetch all rows
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and the database connection
cursor.close()
connection.close()
