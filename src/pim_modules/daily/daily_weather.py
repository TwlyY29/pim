from __future__ import print_function

import configparser
import requests

from datetime import datetime

def format_weather(hourlies, part_of_day='morning'):
  
  min_h = min(h['dt_hour'] for h in hourlies)
  max_h = max(h['dt_hour'] for h in hourlies)
  min_p = min(h['pop'] for h in hourlies) * 100
  max_p = max(h['pop'] for h in hourlies) * 100
  min_w = round(min(h['wind_speed'] for h in hourlies))
  max_w = round(max(h['wind_speed'] for h in hourlies))
  prec = f"{min_p:.0f}-{max_p:.0f}%" if min_p != max_p else f"{min_p:.0f}%"
  wind = f"{min_w}-{max_w} m/s" if min_w != max_w else f"{min_w} m/s"
  min_t = round(min(h['temp'] for h in hourlies))
  max_t = round(max(h['temp'] for h in hourlies))
  temp = f" ({min_t}-{max_t}°)" if min_t != max_t else ''
  avg = round(sum(h['temp'] for h in hourlies) / len(hourlies), 1)
  
  wthr_descr = [h['weather'][0]['description'] for h in hourlies]
  max_wd = max(set(wthr_descr), key=wthr_descr.count)
  
  return f"""...during {part_of_day} ({min_h}-{max_h}):
  {avg}°{temp}, {prec} rain, {wind} wind, mostly {max_wd}"""

def build_url(lon,lat,apikey):
  return f"https://api.openweathermap.org/data/2.5/onecall?lon={lon}&lat={lat}&exclude=current,minutely&units=metric&APPID={apikey}"

def compile_output(conf_sec, CONF_FILE):
  output = ''
  title = None
  config = configparser.ConfigParser()
  config.read(CONF_FILE)
  if config.has_section(conf_sec):
    LOCATION = config[conf_sec]['where']
    API_CALL = build_url(config[conf_sec]['lon'],config[conf_sec]['lat'],config[conf_sec]['api_key'])
  
    today = datetime.now()
  
    try:
      resp = requests.get(API_CALL)
      if resp.status_code == 200:
        json = resp.json()
        weather_morning = []
        weather_midday = []
        weather_evening = []
        for hourly in json['hourly']:
          dt = datetime.fromtimestamp(hourly['dt'])
          if dt.day != today.day or dt.month != today.month:
            continue
          hourly['dt_hour'] = dt.hour
          if dt.hour >= 6 and dt.hour <= 11 and today.hour <= 11:
            weather_morning.append(hourly)
          elif dt.hour >= 12 and dt.hour <= 16 and today.hour <= 16:
            weather_midday.append(hourly)
          elif dt.hour >= 17 and dt.hour <= 23 and today.hour <= 23:
            weather_evening.append(hourly)
        
        morning = '  '+format_weather(weather_morning).replace('\n', '\n  ') if len(weather_morning) > 0 else ''
        midday  = '  '+format_weather(weather_midday, "midday").replace('\n', '\n  ') if len(weather_midday) > 0 else ''
        evening = '  '+format_weather(weather_evening, "evening").replace('\n', '\n  ') if len(weather_evening) > 0 else ''
        
        title = f"Today's weather in {LOCATION}..."
        # ~ output = f"{morning}\n{midday}\n{evening}\n\n"
        if morning != '':
          output += morning + '\n'
        if midday != '':
          output += midday + '\n'
        if evening != '':
          output += evening + '\n'
    except Exception as e:
      print(e)
  if output != '':
    return title,output
  else:
    return title,False

if __name__ == '__main__':
  print(daily_weather('daily_weather_1'))
