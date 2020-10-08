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

from django.test import TestCase
from django.utils import timezone

from . import models


class CouncilTestCase(TestCase):
    def setUp(self):
        self.voter1 = models.Voter.objects.create(name="Voter One", is_active=True)
        self.voter2 = models.Voter.objects.create(name="Voter Two", is_active=True)
        self.voter3 = models.Voter.objects.create(name="Voter Three", is_active=False)

    def test_create_votes(self):
        models.Poll.objects.create(
            question="Question?",
        )
        self.assertEqual(models.Vote.objects.all().count(), 2)
        self.assertFalse(models.Vote.objects.filter(voter=self.voter3).exists())

    def test_close_poll_when_all_voted(self):
        poll = models.Poll.objects.create(
            question="Question?",
        )
        yes = models.Choice.objects.create(
            poll=poll,
            text="Yes",
        )
        models.Choice.objects.create(
            poll=poll,
            text="No",
        )
        self.assertTrue(poll.is_open)
        for vote in poll.votes.all():
            vote.record_choice(yes.id)
        self.assertFalse(models.Poll.objects.get(id=poll.id).is_open)

    def test_no_voting_after_close(self):
        poll = models.Poll.objects.create(
            question="Question?",
            end_datetime=timezone.now() - timezone.timedelta(days=1),
        )
        yes = models.Choice.objects.create(
            poll=poll,
            text="Yes",
        )
        models.Choice.objects.create(
            poll=poll,
            text="No",
        )
        with self.assertRaises(poll.PollClosed):
            for vote in poll.votes.all():
                vote.record_choice(yes.id)

    def test_no_voting_multiple_times(self):
        poll = models.Poll.objects.create(
            question="Question?",
            is_anonymous=False,
        )
        yes = models.Choice.objects.create(
            poll=poll,
            text="Yes",
        )
        models.Choice.objects.create(
            poll=poll,
            text="No",
        )
        vote = poll.votes.get(voter=self.voter1)
        vote.record_choice(yes.id)
        with self.assertRaises(vote.AlreadyVoted):
            vote.record_choice(yes.id)

    def test_anonymize(self):
        poll = models.Poll.objects.create(
            question="Question?",
        )
        yes = models.Choice.objects.create(
            poll=poll,
            text="Yes",
        )
        models.Choice.objects.create(
            poll=poll,
            text="No",
        )
        vote = poll.votes.get(voter=self.voter1)
        self.assertTrue(vote.voter)
        self.assertTrue(vote.key)
        vote.record_choice(yes.id)
        self.assertFalse(vote.voter)
        self.assertFalse(vote.key)
        with self.assertRaises(models.Vote.DoesNotExist):
            vote = poll.votes.get(voter=self.voter1)

    def test_no_anonymize(self):
        poll = models.Poll.objects.create(
            question="Question?",
            is_anonymous=False,
        )
        yes = models.Choice.objects.create(
            poll=poll,
            text="Yes",
        )
        models.Choice.objects.create(
            poll=poll,
            text="No",
        )
        vote = poll.votes.get(voter=self.voter1)
        self.assertTrue(vote.voter)
        self.assertTrue(vote.key)
        vote.record_choice(yes.id)
        self.assertTrue(vote.voter)
        self.assertTrue(vote.key)
        vote_again = poll.votes.get(voter=self.voter1)
        self.assertTrue(vote_again.voter)
        self.assertTrue(vote_again.key)
