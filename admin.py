from django.contrib import admin
from .models import WardrobeItem
from django.contrib import admin
from .models import ColorCombination

admin.site.register(ColorCombination)


@admin.register(WardrobeItem)
class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'article_type', 'base_colour', 'season', 'usage')
    search_fields = ('user__username', 'article_type', 'base_colour', 'season', 'usage')
