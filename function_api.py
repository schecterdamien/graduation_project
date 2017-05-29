import requests
import json

API_KEY = 'ba3df71c201549cde3c66b3581eedb24'
API_URL = 'http://v.juhe.cn/weather/index'


def weather_request(city):
    weather_data = {}
    params = {'cityname': city,
              'key': API_KEY}
    result = requests.get(url=API_URL, params=params)
    result_json = result.json()
    weather_data['temp'] = result_json['result']['sk']['temp']
    weather_data['wind_direction'] = result_json['result']['sk']['wind_direction']
    weather_data['wind_strength'] = result_json['result']['sk']['wind_strength']
    weather_data['humidity'] = result_json['result']['sk']['humidity']
    weather_data['time'] = result_json['result']['sk']['time']
    weather_data['city'] = result_json['result']['today']['city']
    weather_data['temperature'] = result_json['result']['today']['temperature']
    weather_data['weather'] = result_json['result']['today']['weather']
    weather_data['dressing_index'] = result_json['result']['today']['dressing_index']
    weather_data['dressing_advice'] = result_json['result']['today']['dressing_advice']

    print(weather_data)
    return weather_data


def weather_response(city):
    weather_data = weather_request(city)
    response = ('小z天气查询\n'
                '城市名称：{0[city]}\n'
                '当前温度：{0[temp]}度\n'
                '风向：{0[wind_direction]}\n'
                '风力：{0[wind_strength]}\n'
                '湿度：{0[humidity]}\n'
                '更新时间：{0[time]}\n'
                '今日温度：{0[temperature]}\n'
                '天气：{0[weather]}\n'
                '气温描述：{0[dressing_index]}\n'
                '着装建议：{0[dressing_advice]}')
    response = response.format(weather_data)
    return response
if __name__ == '__main__':
    weather_response('武汉')
