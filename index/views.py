from django.shortcuts import render
from django.views.generic import TemplateView

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
