from langchain_core.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from dotenv import load_dotenv
from data_models.models import WeatherApiSchema

load_dotenv()

@tool(args_schema=WeatherApiSchema)
def get_weather_data(city:str):
    """
    Give the city name and get 
    all real weather info about the 
    city underconsideration
    """
    
    weather = OpenWeatherMapAPIWrapper()
    
    weather_data = weather.run(city)
    
    return weather_data

if __name__ == "__main__":
    weather_data = get_weather_data("Hyderabad")
    print(weather_data)
    
    