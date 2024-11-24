import random
from .models import WardrobeItem, ColorCombination
from .weather_utils import get_weather


def get_outfit_suggestions(user, occasion, city):
    api_key = '4137de9aff161b5157d0ad5c653f7d6c'  # Replace with your OpenWeatherMap API key
    weather = get_weather(api_key, city)

    temperature = weather['temperature']
    description = weather['description']

    # Base filtering by weather
    if temperature < 25:
        # Summer outfits
        topwear = WardrobeItem.objects.filter(user=user, article_type='Shirts')
        bottomwear = WardrobeItem.objects.filter(user=user, article_type='Jeans')
    elif temperature > 15 and temperature<20:
        # Winter outfits
        topwear = WardrobeItem.objects.filter(user=user, article_type='Shirts')
        bottomwear = WardrobeItem.objects.filter(user=user, article_type='Track Pants')
    else:
        # Spring/Autumn outfits
        topwear = WardrobeItem.objects.filter(user=user, article_type='Shirts')
        bottomwear = WardrobeItem.objects.filter(user=user, article_type='Track Pants')

    # Filter by occasion
    if occasion == 'Casual':
        topwear = topwear.filter(usage='Casual')
        bottomwear = bottomwear.filter(usage='Casual')
    elif occasion == 'Formal':
        topwear = topwear.filter(usage='Formal')
        bottomwear = bottomwear.filter(usage='Casual')

    print("Topwear:", list(topwear.values_list('id', 'base_colour')))
    print("Bottomwear:", list(bottomwear.values_list('id', 'base_colour')))

    # Verify stored color combinations
    color_combinations = ColorCombination.objects.all()
    print("Stored color combinations:", list(color_combinations.values_list('top_color', 'bottom_color')))

    # Find matching color combinations
    suggestions = []
    for combo in color_combinations:
        print(f"Trying color combination: Top Color: {combo.top_color}, Bottom Color: {combo.bottom_color}")

        top_items = topwear.filter(base_colour__iexact=combo.top_color)
        bottom_items = bottomwear.filter(base_colour__iexact=combo.bottom_color)

        print("Top items with color", combo.top_color, ":", list(top_items.values_list('id', 'base_colour')))
        print("Bottom items with color", combo.bottom_color, ":", list(bottom_items.values_list('id', 'base_colour')))

        for top in top_items:
            for bottom in bottom_items:
                suggestions.append((top, bottom))
                if len(suggestions) >= 1:
                    break
            if len(suggestions) >= 1:
                break
        if len(suggestions) >= 1:
            break

    print("Suggestions:", suggestions)

    return suggestions
