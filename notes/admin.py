from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'slug',
        'author',
    )
    list_filter = ('title', 'author',)
    list_display_links = ('title',)
