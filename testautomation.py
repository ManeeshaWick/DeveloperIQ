import pytest
import requests

def test_github_api_status():
    # Call the GitHub API to check its status
    response = requests.get('https://github.com/Trinea/android-open-project')
    
    # Assert the status code
    assert response.status_code == 200
