from django.db import models
from django.db.models.deletion import PROTECT
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Найменування')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=PROTECT, null=True)
    views  = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='модель новина'
        verbose_name_plural = 'новини'
    
    def get_absolute_url(self):
        return reverse('full_news', kwargs={'pk':self.pk})
        

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Найменування категорії')

    def get_absolute_url(self):
        return reverse('choosen_category', kwargs={'a_tag':self.pk})

    class Meta:
        verbose_name='Категорії'
        verbose_name_plural = 'Категорія'
        
        
    def __str__(self):
        return self.title