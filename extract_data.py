import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(API_URL)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

df.to_csv("/tmp/jsonplaceholder_data.csv", index=False)
print("Data saved to /tmp/jsonplaceholder_data.csv")
