import plotly.express as px
import json
forecast_from_server = {}
with open('forecast.json', 'r', encoding='utf-8') as f:
    forecast_from_server = json.load(f)

forecast = forecast_from_server['list']
date_time=[]
temp = []
# clouds = []
# humidity = []
# forecast_clean = []
for dt in forecast:
    date_time.append(dt['dt_txt'])
    temp.append(dt['main']['temp'])
    # clouds.append(dt['clouds']['all'])
    # forecast_clean.append({'dt': dt['dt_txt'], 'temp': dt['main']['temp'], 'humidity': dt['main']['humidity'], 'clouds': dt['clouds']['all']})
    # print(dt)

# print(forecast_clean)
fig = px.line(x=date_time, y=temp)

fig.show()
