"""alita_index URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from contact_form.views import ContactFormView, ContactFormSuccessView
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path(
        'contact/success/',
        ContactFormSuccessView.as_view(),
        name='contact-success',
    ),
    path('index-api/', include('index.api.urls')),
    path('newest/', views.NewestView.as_view(), name='newest'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('rss/', views.RssView.as_view(), name='rss'),
    path('alita-index.md', views.MarkdownView.as_view(), name='markdown'),
    path('captcha/', include('captcha.urls')),
    path('', views.CategoriesView.as_view(), name='categories'),
]
