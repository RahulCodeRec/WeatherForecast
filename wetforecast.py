import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import folium
import requests
import webbrowser
import os

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = "fd9eebf9e01d5da39be4066a012dbdbb"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", data.get("message", "Unknown error"))
            return

        weather = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        result = f"Weather: {weather}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
        result_label.config(text=result)

        # Generate map
        map_file = "weather_map.html"
        weather_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon],
                      popup=f"<b>{city}</b><br>{result.replace('\\n', '<br>')}").add_to(weather_map)
        weather_map.save(map_file)

        # Open map in browser
        webbrowser.open(f"file://{os.path.abspath(map_file)}")

    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch weather data: {e}")

# Create main application window
app = tk.Tk()
app.title("Weather Forecast with Map")
app.geometry("850x650")
app.configure(bg="#f0f8ff")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", background="#f0f8ff", font=("Arial", 12))

# GUI Elements
header_label = tk.Label(app, text="Weather Forecast App", font=("Arial", 20, "bold"), bg="#4682b4", fg="white", pady=10)
header_label.pack(fill=tk.X)

frame = tk.Frame(app, bg="#f0f8ff")
frame.pack(pady=20)

city_label = tk.Label(frame, text="Enter City:", font=("Arial", 14), bg="#f0f8ff")
city_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

city_entry = ttk.Entry(frame, font=("Arial", 14))
city_entry.grid(row=0, column=1, padx=10, pady=5)

get_weather_button = ttk.Button(frame, text="Get Weather", command=get_weather)
get_weather_button.grid(row=0, column=2, padx=10, pady=5)

result_frame = tk.Frame(app, bg="#f0f8ff")
result_frame.pack(pady=10)

result_label = tk.Label(result_frame, text="", font=("Arial", 14), justify="left", bg="#f0f8ff")
result_label.pack()

footer_label = tk.Label(app, text="Powered by OpenWeatherMap", font=("Arial", 10), bg="#4682b4", fg="white")
footer_label.pack(fill=tk.X, side=tk.BOTTOM)

# Run the app
app.mainloop()
