import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0420ba1ce2c1360f0a32a036d68c90b6'

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name = new_city).count()

            if existing_city_count == 0:
                form.save()
            else:
                err_msg = 'City already exist!'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': r.get('name'),
            'temperature': r.get('main').get('temp'),
            'description': r.get('weather')[0].get('description'),
            'icon': r.get('weather')[0].get('icon'),
        }
        weather_data.append(city_weather)

    context = {'weather_data':weather_data, 'form': form}

    return render(request, 'get_weather/get_weather.html', context)