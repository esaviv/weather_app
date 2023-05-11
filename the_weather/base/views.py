import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

app_name = "base"

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=45ecd7eb514b06db2b83e0ad6ccd1c15'
    form = CityForm(request.POST or None)
    err_msg = ""
    message = ""
    message_class = ""
    if request.method == "POST":
        if form.is_valid():
            new_city = form.cleaned_data["name"]
            req = requests.get(url.format(new_city)).json()

            if not City.objects.filter(name=new_city).count():
                if req["cod"] == 200:
                    form.save()
                else:
                    err_msg = "City does not exist in the world!"
            else:
                err_msg = "City alredy exists in the database!"

            if err_msg:
                message = err_msg
                message_class = "is-danger"
            else:
                message = "City added succesfully!"
                message_class = "is-success"

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        req = requests.get(url.format(city)).json()

        city_weather = {
            "city": city.name,
            "temperature": req["main"]["temp"],
            "description": req["weather"][0]["description"],
            "icon": req["weather"][0]["icon"],
        }

        weather_data.append(city_weather)

    context = {
        "weather_data": weather_data, 
        "form": form,
        "message": message,
        "message_class": message_class}

    return render(request, "base/weather.html", context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect("base:home")
