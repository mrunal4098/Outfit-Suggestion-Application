# wardrobe/views.py
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WardrobeItemForm
from .models import WardrobeItem
from .ml_utils import predict_image
import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_outfit_suggestions, get_weather
from django.shortcuts import render, redirect
from .models import WardrobeItem, ColorCombination
from .weather_utils import get_weather
from .utils import get_outfit_suggestions
from .forms import OutfitSuggestionForm
from .models import WardrobeItem, ColorCombination

@login_required
def suggest_outfit(request):
    if request.method == 'POST':
        form = OutfitSuggestionForm(request.POST)
        if form.is_valid():
            occasion = form.cleaned_data['occasion']
            location = form.cleaned_data['location']

            # Get current weather for the location
            api_key = '4137de9aff161b5157d0ad5c653f7d6c'  # Replace with your OpenWeatherMap API key
            weather = get_weather(api_key, location)
            print(weather,"os")

            if weather is None:
                # If weather data could not be fetched, show an error message
                return render(request, 'wardrobe/suggest_form.html', {
                    'form': form,
                    'error_message': 'Could not fetch weather data. Please try again later.'
                })
            print(weather['temperature'],"uv")

            temperature = weather['temperature']
            print(temperature)
            # Get outfit suggestions based on temperature and occasion
            suggestions = get_outfit_suggestions(request.user, occasion, location)

            return render(request, 'wardrobe/suggest_outfit.html', {
                'form': form,
                'suggestions': suggestions,
                'temperature': temperature,
                'occasion': occasion,
                'location': location
            })
    else:
        form = OutfitSuggestionForm()

    return render(request, 'wardrobe/suggest_form.html', {'form': form})




'''@login_required
def upload_image(request):
    if request.method == 'POST':
        form = WardrobeItemForm(request.POST, request.FILES)
        if form.is_valid():
            wardrobe_item = form.save(commit=False)
            wardrobe_item.user = request.user
            wardrobe_item.save()
            # Call the classification function here if needed
            return redirect('home')  # Redirect to a success page
    else:
        form = WardrobeItemForm()
    return render(request, 'wardrobe/upload_image.html', {'form': form})'''

@login_required
def wardrobe_view(request):
    items = WardrobeItem.objects.filter(user=request.user)
    return render(request, 'wardrobe/wardrobe.html', {'items': items})

@login_required
def upload_image(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            wardrobe_item = WardrobeItem(user=request.user, image=image)
            wardrobe_item.save()

            # Get the path to the uploaded image
            image_path = wardrobe_item.image.path

            # Classify the image
            decoded_predictions, predictions = predict_image(image_path)

            # Save the predictions to the model instance
            wardrobe_item.article_type = decoded_predictions[0]
            wardrobe_item.base_colour = decoded_predictions[1]
            wardrobe_item.season = decoded_predictions[2]
            wardrobe_item.usage = decoded_predictions[3]
            wardrobe_item.save()

        return redirect('home_view')
    return render(request, 'wardrobe/upload_image.html')

@login_required
def wardrobe(request):
    wardrobe_items = WardrobeItem.objects.filter(user=request.user)
    return render(request, 'wardrobe/wardrobe.html', {'wardrobe_items': wardrobe_items})
