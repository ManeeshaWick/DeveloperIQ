import pyodbc
import requests
import pandas as pd

# Retrieving data from the API

def get_commit_stats(repo_url):
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    # Get commit statistics
    commit_url = f"https://api.github.com/repos/{owner}/{repo_name}/stats/contributors"
    commit_response = requests.get(commit_url)

    if commit_response.status_code == 200:
        contributors_data = commit_response.json()

        commit_data = []
        for contributor in contributors_data:
            author = contributor['author']['login']
            commits = contributor['total']
            commit_data.append({'Author': author, 'Commits': commits})

        # Get issues statistics
        issues_url = f"https://api.github.com/repos/{owner}/{repo_name}/issues?state=closed"
        issues_response = requests.get(issues_url)

        if issues_response.status_code == 200:
            issues_data = issues_response.json()

            issues_count = {}
            for issue in issues_data:
                author = issue['user']['login']
                if issue.get('pull_request'):
                    if author in issues_count:
                        issues_count[author] += 1
                    else:
                        issues_count[author] = 1

            for item in commit_data:
                author = item['Author']
                item['IssuesSolved'] = issues_count.get(author, 0)

            # Get pull requests statistics
            pulls_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=closed"
            pulls_response = requests.get(pulls_url)

            if pulls_response.status_code == 200:
                pulls_data = pulls_response.json()

                pulls_count = {}
                for pull in pulls_data:
                    author = pull['user']['login']
                    if author in pulls_count:
                        pulls_count[author] += 1
                    else:
                        pulls_count[author] = 1

                for item in commit_data:
                    author = item['Author']
                    item['PullRequests'] = pulls_count.get(author, 0)

                return commit_data
            else:
                print(f"Failed to fetch pull requests data: {pulls_response.status_code} - {pulls_response.text}")
                return None
        else:
            print(f"Failed to fetch issues data: {issues_response.status_code} - {issues_response.text}")
            return None
    else:
        print(f"Failed to fetch commit data: {commit_response.status_code} - {commit_response.text}")
        return None

repo_url = "https://github.com/Trinea/android-open-project"

commit_stats = get_commit_stats(repo_url)
if commit_stats:
    commit_stats_df = pd.DataFrame(commit_stats)

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

def _insert_data():
    try:
        # Connect to the database
        conn = connect_db()
        
        # Create a cursor
        cursor = conn.cursor()

        # Delete existing data from dbo.github_developer_data table
        cursor.execute("DELETE FROM dbo.github_developer_data")
        conn.commit()

        # Insert data from the DataFrame into the database
        for index, row in commit_stats_df.iterrows():
            cursor.execute("INSERT INTO dbo.github_developer_data (developer_name, no_of_commits, no_of_issues, no_of_requests) VALUES (?, ?, ?, ?)",
                           row['Author'], row['Commits'], row['IssuesSolved'], row['PullRequests'])
        conn.commit()
                      
        # Close the cursor and connection
        cursor.close()
        conn.close()
    
    except Exception as e:
        return str(e)




