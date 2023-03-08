import requests

# Set up the URL for the API endpoint
url = "https://www.aavso.org/apps/vsp/api/chart/"

# Set up the parameters for the API request
params = {
    "name": "V",
    "ra": "10.68479",
    "dec": "41.26906",
    "fov": "0.1",
    "start": "2022-01-01",
    "stop": "2022-03-01",
    "output": "json"
}

# Make the API request
response = requests.get(url, params=params)

# Print the response
print(response.text)
   
