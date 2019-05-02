from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from . import models


class CategoriesView(TemplateView):
    id = 'categories'
    template_name = 'index/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.filter(
            parent__isnull=True,
        )
        return context


class NewestView(ListView):
    id = 'newest'
    queryset = models.Entry.objects.filter(
        is_visible=True).order_by('-created')
    template_name = 'index/newest.html'
    context_object_name = 'entries'
