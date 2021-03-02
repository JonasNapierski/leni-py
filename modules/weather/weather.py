import json 
import requests

with open("modules/weather/module.json", "r") as f:
    cfg = json.loads(f.read())



def exec(msg):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}"
    api_url = api_url.replace("{API key}", cfg['api_token'])

    print(msg)
    city = ""
    mm = msg.split(" ")
    print(mm)
    for i in range(len(mm)):
        if mm[i] == "in":
            city = mm[i+1]
               
                
    api_url = api_url.replace("{city name}", city)

    data = requests.post(api_url).json()
    temp = float(data['main']['temp'])
    temp = temp - 273.15
    #return data
    return {"temp": temp, "msg": f"In {city} sind es {temp:.2f}°c"}