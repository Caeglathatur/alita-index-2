"""
Copyright © 2019-2020 Alita Index / Caeglathatur

This file is part of Alita Index.

Alita Index is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Alita Index is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Alita Index.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from . import models


class CouncilIndex(TemplateView):
    template_name = "council/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voters"] = models.Voter.objects.filter(is_active=True).order_by("name")
        return context


class PollDetailView(DetailView):
    model = models.Poll
    queryset = models.Poll.objects.filter(is_public=True)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=self.kwargs.get("pk"))
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context, status=200 if self.object else 404)


class VoteSuccessView(TemplateView):
    template_name = "council/vote_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poll"] = self.kwargs.get("pk")
        return context


class VoteDetailView(DetailView):
    model = models.Vote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["object"]:
            context["poll"] = context["object"].poll
            context["has_voted"] = bool(context["object"].choice)
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get(key=self.kwargs.get("key"))
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context, status=200 if self.object else 404)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        choice_id = request.POST.get("choice", None)

        choice_invalid_msg = "Your choice was invalid."

        if not choice_id:
            context["error"] = choice_invalid_msg
            return self.render_to_response(context, status=400)

        try:
            self.object.record_choice(choice_id)
        except models.Poll.PollClosed:
            context["error"] = "The poll is closed. Your vote has not been counted."
            return self.render_to_response(context, status=403)
        except models.Vote.AlreadyVoted:
            # The regular voting page, once reloaded, will say that the user has
            # already voted
            return self.render_to_response(context, status=403)
        except models.Vote.InvalidChoice:
            context["error"] = choice_invalid_msg
            return self.render_to_response(context, status=400)

        return redirect("vote-success", pk=self.object.poll.pk)
