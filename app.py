from flask import Flask, render_template
import pyodbc
import requests
import pandas as pd

app = Flask(__name__, template_folder= 'template')

# Database configuration for SQL Server
DB_CONFIG = {
    'server': 'developeriq-db.ceojxcofakbp.us-east-1.rds.amazonaws.com',  
    'database': 'developeriq',
    'username': 'admin',
    'password': 'maneesha',
    'driver': '{ODBC Driver 17 for SQL Server}',  
}

# Connect to the database
def connect_db():
    return pyodbc.connect(
        f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
    )

# Route to display the table
@app.route('/')
def display_table():
    try:
        # Connect to the database
        conn = connect_db()
        
        # Create a cursor
        cursor = conn.cursor()
       
        # Execute a query to fetch data
        cursor.execute("SELECT developer_name, no_of_commits, no_of_issues, no_of_requests FROM dbo.github_developer_data")
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Pass the data to the template
        return render_template('table.html', data=rows)
    
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


#changing to push



