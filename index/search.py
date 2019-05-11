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

from . import models


search_fields = {
    'Entry': [
        'title',
        'description',
        # 'url',
    ],
    'SubEntry': [
        'title',
        'description',
        # 'url',
    ],
    'Category': [
        'name',
    ],
    'Tag': [
        'name',
    ],
    'Author': [
        'name',
    ],
    'EntryIdentifier': [
        'value',
    ],
    'SubEntryIdentifier': [
        'value',
    ],
}


def add_hit(dict, key, term):
    if key not in dict:
        dict[key] = {term}
    else:
        dict[key].add(term)


def search_entries(query):
    """:returns: ordered list of (<Entry>, <number of unique hit terms>)"""

    terms = query.lower().split()
    if not terms:
        return []

    hits = {}  # {<Entry>: {<terms>}}

    entries = models.Entry.objects.filter(is_visible=True)
    sub_entries = models.SubEntry.objects.all()
    categories = models.Category.objects.all()
    authors = models.Author.objects.all()
    tags = models.Tag.objects.all()
    entry_identifiers = models.EntryIdentifier.objects.all()
    sub_entry_identifiers = models.SubEntryIdentifier.objects.all()

    # Search in entries
    for e in entries:
        for field in search_fields['Entry']:
            if not hasattr(e, field):
                continue
            content = getattr(e, field).lower()
            for term in terms:
                if term in content:
                    add_hit(hits, e, term)

    # Search in sub entries
    for s in sub_entries:
        for field in search_fields['SubEntry']:
            if not hasattr(s, field):
                continue
            content = getattr(s, field).lower()
            for term in terms:
                if term in content:
                    add_hit(hits, s.entry_traversed, term)

    # Search in categories
    for c in categories:
        for field in search_fields['Category']:
            if not hasattr(c, field):
                continue
            content = getattr(c, field).lower()
            for term in terms:
                if term in content:
                    for e in c.entries_visible_traversed:
                        add_hit(hits, e, term)

    # Search in authors
    for a in authors:
        for field in search_fields['Author']:
            if not hasattr(a, field):
                continue
            content = getattr(a, field).lower()
            for term in terms:
                if term in content:
                    for e in a.entries_visible:
                        add_hit(hits, e, term)

    # Search in tags
    for t in tags:
        for field in search_fields['Category']:
            if not hasattr(t, field):
                continue
            content = getattr(t, field).lower()
            for term in terms:
                if term in content:
                    for e in t.entries_visible:
                        add_hit(hits, e, term)

    # Search in entry identifiers
    for i in entry_identifiers:
        for field in search_fields['EntryIdentifier']:
            if not hasattr(i, field):
                continue
            content = getattr(i, field).lower()
            for term in terms:
                if term in content:
                    add_hit(hits, i.entry, term)

    # Search in sub entry identifiers
    for i in sub_entry_identifiers:
        for field in search_fields['SubEntryIdentifier']:
            if not hasattr(i, field):
                continue
            content = getattr(i, field).lower()
            for term in terms:
                if term in content:
                    add_hit(hits, i.entry, term)

    # Only return visible entries
    hits = list(filter(
        lambda e: e[0].is_visible,
        hits.items(),
    ))
    # Replace hit sets with hit counts
    hits = list(map(
        lambda e: (e[0], len(e[1])),
        hits,
    ))
    # Sort by hit count and entry title
    hits = sorted(hits, key=lambda e: (e[1], e[0].title), reverse=True)

    return hits
