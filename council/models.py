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

from functools import partial

from django.apps import apps
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string


def _unique_random_string(unique_for_model_name, prop, length):
    string = get_random_string(length)
    model = apps.get_app_config("council").get_model(unique_for_model_name)
    try:
        model.objects.get(**{prop: string})
        return _unique_random_string(unique_for_model_name, prop, length)
    except model.DoesNotExist:
        return string


class Poll(models.Model):
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(_unique_random_string, "Poll", "id", 10),
    )
    question = models.TextField()
    is_public = models.BooleanField(
        default=True, help_text="Poll detail view is publicly accessible."
    )
    is_anonymous = models.BooleanField(
        default=True,
        help_text=(
            "If set during voting, voter identifiers are erased from the votes when "
            "they are cast. If set, individual votes are not shown publicly."
        ),
    )
    end_datetime = models.DateTimeField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class PollClosed(Exception):
        pass

    @property
    def is_open(self) -> bool:
        return not self.end_datetime or timezone.now() < self.end_datetime

    @property
    def cast_votes_count(self) -> int:
        return self.votes.filter(choice__isnull=False).count()

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse_lazy("poll-detail", args=[self.id])

    def save(self, *args, **kwargs):
        adding = self._state.adding
        super().save(*args, **kwargs)
        if adding:
            for voter in Voter.objects.filter(is_active=True):
                Vote.objects.create(
                    poll=self,
                    voter=voter,
                )


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def votes_percentage(self) -> str:
        return f"{self.votes.all().count() * 100 / self.poll.votes.all().count():.1f}"

    def __str__(self):
        return self.text


class Voter(models.Model):
    name = models.CharField(max_length=200)
    polls_voter_of = models.ManyToManyField(Poll, through="Vote")
    is_public = models.BooleanField(
        default=False, help_text="Show this voter's name publicly."
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Create votes for this voter when creating new polls, and show among "
            "voters."
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def public_name(self) -> str:
        return self.name if self.is_public else "< hidden >"

    def __str__(self):
        return self.name


class Vote(models.Model):
    key = models.CharField(
        max_length=50,
        default=partial(_unique_random_string, "Vote", "key", 20),
        null=True,
        blank=True,
    )
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(
        Voter,
        on_delete=models.DO_NOTHING,
        related_name="votes",
        null=True,
        blank=True,
        default=None,
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        related_name="votes",
        null=True,
        blank=True,
        default=None,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class AlreadyVoted(Exception):
        pass

    class InvalidChoice(Exception):
        pass

    def get_absolute_url(self):
        return reverse_lazy("vote-detail", args=[self.key]) if self.key else None

    def __str__(self):
        return "{} - {}: {}".format(self.poll, self.voter, self.choice)

    def record_choice(self, choice_id):
        if self.choice:
            raise self.AlreadyVoted()

        if not self.poll.is_open:
            raise Poll.PollClosed()

        try:
            choice = Choice.objects.get(poll=self.poll, id=choice_id)
        except Choice.DoesNotExist:
            raise self.InvalidChoice()

        self.choice = choice
        if self.poll.is_anonymous:
            self.voter = None
            self.key = None
        self.save()

        # Close poll if all votes have been cast
        if not self.poll.votes.filter(choice__isnull=True).exists():
            self.poll.end_datetime = timezone.now()
            self.poll.save()
