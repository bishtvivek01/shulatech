# import tkinter as tk
# import requests

# API_KEY = "d62ad69f5e50219c15fbb96643bd1e74"  

# def get_weather():
#     city = city_entry.get()
#     if city:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             weather_info.set(f"Temperature: {data['main']['temp']}°C\n"
#                              f"Humidity: {data['main']['humidity']}%\n"
#                              f"Condition: {data['weather'][0]['description'].title()}")
#         else:
#             weather_info.set("City not found!")

# # GUI setup
# root = tk.Tk()
# root.title("Weather App")

# tk.Label(root, text="Enter City:").pack()
# city_entry = tk.Entry(root)
# city_entry.pack()

# tk.Button(root, text="Get Weather", command=get_weather).pack()

# weather_info = tk.StringVar()
# tk.Label(root, textvariable=weather_info, font=("Arial", 14)).pack()

# root.mainloop()

import tkinter as tk
import requests

API_KEY = "d62ad69f5e50219c15fbb96643bd1e74"

def get_weather():
    city = city_entry.get()
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_info.set(f"Temperature: {data['main']['temp']}°C\n"
                             f"Humidity: {data['main']['humidity']}%\n"
                             f"Condition: {data['weather'][0]['description'].title()}")
        else:
            weather_info.set("City not found!")

def get_forecast():
    city = city_entry.get()
    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_text = "7-Day Forecast:\n"
            for item in data["list"][:7]:
                forecast_text += f"{item['dt_txt']} - {item['main']['temp']}°C, {item['weather'][0]['description'].title()}\n"
            weather_info.set(forecast_text)
        else:
            weather_info.set("City not found!")

root = tk.Tk()
root.title("Weather App")

city_entry = tk.Entry(root, width=30)
city_entry.pack()
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack()
get_forecast_button = tk.Button(root, text="Get 7-Day Forecast", command=get_forecast)
get_forecast_button.pack()

weather_info = tk.StringVar()
weather_label = tk.Label(root, textvariable=weather_info, width=50, height=10)
weather_label.pack()

root.mainloop()
