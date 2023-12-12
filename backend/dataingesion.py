from github import Github
import pandas as pd
import sqlalchemy

# GitHub repository information
repo_url = "https://github.com/practical-tutorials/project-based-learning"

# SQL Server credentials
sql_credentials = {
    'server': 'developeriq-db.ceojxcofakbp.us-east-1.rds.amazonaws.com',
    'database': 'developeriq',
    'username': 'admin',
    'password': 'maneesha',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

# Connect to GitHub using PyGithub library
g = Github()

# Get the repository
repo = g.get_repo(repo_url.replace("https://github.com/", ""))

# Initialize empty lists to store data
developer_names = []
no_of_commits = []
no_of_issues = []
no_of_requests = []

# Fetch data for each contributor
contributors = repo.get_contributors()
for contributor in contributors:
    developer_names.append(contributor.login)
    no_of_commits.append(repo.get_commits(author=contributor).totalCount)
    no_of_issues.append(repo.get_issues(creator=contributor).totalCount)
    no_of_requests.append(repo.get_pulls(user=contributor.login, state='all').totalCount)

# Create a DataFrame
data = {
    'developer_name': developer_names,
    'no_of_commits': no_of_commits,
    'no_of_issues': no_of_issues,
    'no_of_requests': no_of_requests
}
df = pd.DataFrame(data)

# Connect to SQL Server and ingest data into the specified table
engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://{sql_credentials['username']}:{sql_credentials['password']}@{sql_credentials['server']}/{sql_credentials['database']}?driver={sql_credentials['driver']}"
)
df.to_sql('your_table_name', con=engine, if_exists='replace', index=False)
