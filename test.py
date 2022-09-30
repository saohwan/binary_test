import requests

data = {
    "ossName": "jdbc14.jar"
}
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AZm9zc2xpZ2h0Lm9yZyJ9.3jWpmXwz73emxQ6tYjf1nkecLK3Br6Jth08trgF-gxQ'
header = {"Content-Type": "application/json",
          "_token": {key}.format(key=api_key)}

vulnerability_data = requests.post("https://demo.fosslight.org/api/v1/vulnerability_max_data", headers=header,
                                   params=data)

print(vulnerability_data)
