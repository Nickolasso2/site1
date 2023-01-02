from dataclasses import fields
from pyexpat import model
from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class NewsEditable(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model= News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsEditable
    list_display = ('title','is_published', 'listtest')
    list_display_links = ('title',)
    search_fields = ('content',)
    list_editable = ('is_published',)
    list_filter =('title', 'content')

    def listtest (self, object):
        return object.title.upper()

    
    listtest.short_description = 'added'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)




admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'Changed admin title with admin.py'
admin.site.site_header = 'Керування сайтом(змінено в admin.py) '