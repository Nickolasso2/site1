from re import template
import re
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import NewNews, NewCategory, MyRegisterForm, MyLog_inForm, SendMailForm
from .models import News, Category
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

def index(request):
    news = News.objects.all().select_related('category')
    
    # ______pagination for function_____
    paginator = Paginator(news, 4)
    page_number = request.GET.get('page', 1)# equals page to 1, if there is no page value
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'myapp1/index.html', {'news': news, 'var2': 'Головна. Всі категорії', 'page_obj': page_obj})


def index2(request):
    return HttpResponse('<h1>я індекс2 функція</h1>')


def index0(request):
    return HttpResponse('<h1>я empty url</h1>')


def get_category(request, a_tag):
    news = News.objects.filter(category=a_tag)
    category = Category.objects.get(pk=a_tag)
    return render(request, 'myapp1/category.html', {'news': news, 'category': category, 'var2': 'category:' + f'{category}'})


# def get_full_news(request, news_id):
#     news = News.objects.get(pk=news_id)
#     return render(request, 'myapp1/full_news.html', {'news': news})

@login_required(login_url='/admin/')
def add_news(request):
    if request.method == 'POST':
        form = NewNews(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            n = News.objects.create(**form.cleaned_data)
            return redirect('add_news')
    else:
        form = NewNews()
    return render(request, 'myapp1/add_news.html', {'form': form})



def add_category(request):
    if request.method == 'POST':
        form = NewCategory(request.POST)
        # print(form, '\n', type(form))виведення у консоль
        if form.is_valid():
            n = form.save()
            print(type(form), '\n', type(n))
            return redirect()
    else:
        form = NewCategory()
    return render(request, 'myapp1/add_category.html', {'form': form})


class NewsView(ListView):
    model = News
    template_name = 'myapp1/navbar.html'
    context_object_name = 'news'
    extra_context = {'dir1': 'dd1'}
    
    

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['dir2'] = 'get context data value252'
        return c

    def get_queryset(self):
        n = News.objects.filter(title='d')
        return n


class NewsCategory(ListView):
    model = News
    paginate_by = 1
    # allow_empty = False
  

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['title'] = Category.objects.get(pk=self.kwargs['a_tag'])
        return c

    def get_queryset(self):
        return News.objects.filter(category=self.kwargs['a_tag']).select_related('category')
        
class NewsDetail(DetailView):
    model = News
    

# class CreateCategory(CreateView):
#     form_class = NewCategory
#     template_name = 'myapp1/add_category.html'
#     success_url = reverse_lazy('all_category')

# these class and link are not displayed for unauthenticated user
class CreateCategory(LoginRequiredMixin, CreateView):
    form_class = NewCategory 
    template_name = 'myapp1/add_category.html'
    success_url = reverse_lazy('all_category')
    login_url = '/admin/'
    raise_exception = True


# registration form by default UserCreationForm
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Ви зареєстровані')
#             return redirect('log_in')
#         else:
#             messages.error(request, 'Помилка реєстрації')
#     else:
#         form = UserCreationForm()
#     return render(request, 'myapp1/register.html', {'form': form})

# def log_in(request):
#     return render(request, 'myapp1/log_in.html')


# registration form by changed default form UserCreationForm
def register(request):
    if request.method == 'POST':
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # instant authentication
            # user = form.save()
            # login(request, user) 
            messages.success(request, 'Ви зареєстровані')
            return redirect('log_in')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = MyRegisterForm()
    return render(request, 'myapp1/register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = MyLog_inForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('all_category')
    else:
        form = MyLog_inForm()
    return render(request, 'myapp1/log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('all_category')

def mail_sending(request):
    if request.method == 'POST':
        form = SendMailForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subj'], form.cleaned_data['conten'], 'petropetrovic1000@gmail.com', ['tooweird@meta.ua'], fail_silently=False)
            if mail:
                messages.success(request, 'Лист відправлено')
                return redirect('sending_mail')
            else:
                messages.error(request, 'Помилка відправки')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = SendMailForm()
        return render(request, 'myapp1/sending_form.html', {'form': form})

