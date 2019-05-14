"""
Copyright © 2019 Alita Index / Caeglathatur

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

from django.db import models


class Message(models.Model):
    message = models.TextField(verbose_name="message", max_length=1000)
    subject = models.ForeignKey(
        "Subject", verbose_name="subject", on_delete=models.SET_NULL, null=True
    )
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Subject(models.Model):
    class Meta:
        ordering = ["order", "name"]

    name = models.CharField(max_length=150)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
