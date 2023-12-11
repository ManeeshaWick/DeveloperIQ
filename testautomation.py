import requests

def test_github_api():
    url = 'https://api.github.com/repos/Trinea/android-open-project/'
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to access {url}. Status code: {response.status_code}"